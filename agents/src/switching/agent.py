import pickle
import pandas as pd
import requests
import __main__

# =====================================================================
# 1. Redéfinition obligatoire de la classe pour Pickle
# =====================================================================
class ModelWithThreshold:
    def __init__(self, model, threshold=0.6):
        self.model = model
        self.threshold = threshold

    def predict(self, X):
        probs = self.model.predict_proba(X)[:, 1]
        return (probs > self.threshold).astype(int)

    def predict_proba(self, X):
        return self.model.predict_proba(X)

__main__.ModelWithThreshold = ModelWithThreshold


# =====================================================================
# 2. Classe de l'Agent
# =====================================================================
class Agent:
    def __init__(self, uuid: str, model_path: str = "./switching/pokemon_switch_model.pkl", base_url: str = "https://pokestral.anhilyx.fr/api/poke-env"):
        """
        Initialise l'agent avec l'UUID du match, charge le modèle et configure l'URL de l'API.
        """
        self.uuid = uuid
        self.base_url = base_url
        
        # Chargement du modèle
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)
            
        # Définition des colonnes attendues (hors features calculées et colonnes à drop)
        # Ceci permet de s'assurer que le DataFrame a la bonne forme.
        self.expected_base_columns = [
            "turn", "terrain", "weather", "trick_room", "tailwind_p1", "tailwind_p2", 
            "hazards_p1", "hazards_p2", "screens_p1", "screens_p2", "active_p1", "active_p2",
            "active_p1_atk", "active_p1_def", "active_p1_spa", "active_p1_spd", "active_p1_spe", "active_p1_accuracy", "active_p1_evasion",
            "active_p1_move1", "active_p1_move2", "active_p1_move3", "active_p1_move4",
            "active_p2_atk", "active_p2_def", "active_p2_spa", "active_p2_spd", "active_p2_spe", "active_p2_accuracy", "active_p2_evasion",
            "active_p2_move1", "active_p2_move2", "active_p2_move3", "active_p2_move4",
            "matchup_p1_type1", "matchup_p1_type2", "matchup_p2_type1", "matchup_p2_type2",
            "active_p1_name", "active_p2_name",
            "active_p1_name_hp_stat", "active_p1_name_atk_stat", "active_p1_name_def_stat", "active_p1_name_spa_stat", "active_p1_name_spd_stat", "active_p1_name_spe_stat",
            "active_p2_name_hp_stat", "active_p2_name_atk_stat", "active_p2_name_def_stat", "active_p2_name_spa_stat", "active_p2_name_spd_stat", "active_p2_name_spe_stat"
        ]
        
        # Ajout dynamique des colonnes de la team (A à F)
        for p in ["p1", "p2"]:
            for letter in ["A", "B", "C", "D", "E", "F"]:
                self.expected_base_columns.extend([
                    f"pokemon_{p}{letter}", f"type_1_{p}{letter}", f"type_2_{p}{letter}", 
                    f"hp_{p}{letter}", f"status_{p}{letter}"
                ])

    def _fetch_data(self, endpoint: str):
        """Helper pour appeler l'API."""
        res = requests.get(f"{self.base_url}/look/{endpoint}", params={"uuid": self.uuid})
        res.raise_for_status()
        return res.json()

    def _parse_to_dataframe(self) -> pd.DataFrame:
        """
        Récupère toutes les données via l'API et les aplatit dans un dictionnaire 
        correspondant aux colonnes du dataset d'entraînement.
        """
        # --- 1. Récupération des données ---
        turn_data = self._fetch_data("turn")
        terrain_data = self._fetch_data("terrain")
        active_data = self._fetch_data("active-pokemons")
        teams_data = self._fetch_data("teams")
        moves_data = self._fetch_data("available-moves")
        
        # Initialisation du dictionnaire avec des valeurs par défaut sécurisées
        row = {col: "none" if "type" in col or "move" in col or "pokemon" in col or "name" in col else 0.0 for col in self.expected_base_columns}

        # --- 2. Remplissage basique ---
        row["turn"] = turn_data.get("turn", 1)
        
        # Terrain & Météo (Ajuste les clés selon ton TerrainModel)
        row["terrain"] = terrain_data.get("terrain", "none")
        row["weather"] = terrain_data.get("weather", "none")
        row["trick_room"] = int(terrain_data.get("trick_room", False))
        row["tailwind_p1"] = int(terrain_data.get("p1_side_conditions", {}).get("tailwind", False))
        row["tailwind_p2"] = int(terrain_data.get("p2_side_conditions", {}).get("tailwind", False))
        row["hazards_p1"] = str(terrain_data.get("p1_side_conditions", {}).get("hazards", []))
        row["hazards_p2"] = str(terrain_data.get("p2_side_conditions", {}).get("hazards", []))
        row["screens_p1"] = str(terrain_data.get("p1_side_conditions", {}).get("screens", []))
        row["screens_p2"] = str(terrain_data.get("p2_side_conditions", {}).get("screens", []))

        # --- 3. Pokémons Actifs ---
        # Suppose que active_data renvoie {"p1": {...}, "p2": {...}}
        p1_active = active_data.get("p1", {})
        p2_active = active_data.get("p2", {})
        
        row["active_p1"] = p1_active.get("species", "none")
        row["active_p2"] = p2_active.get("species", "none")
        row["active_p1_name"] = p1_active.get("species", "none")
        row["active_p2_name"] = p2_active.get("species", "none")
        
        # Boosts (Stats modifiers)
        p1_boosts = p1_active.get("boosts", {})
        p2_boosts = p2_active.get("boosts", {})
        for stat in ["atk", "def", "spa", "spd", "spe", "accuracy", "evasion"]:
            row[f"active_p1_{stat}"] = float(p1_boosts.get(stat, 0.0))
            row[f"active_p2_{stat}"] = float(p2_boosts.get(stat, 0.0))
            
        # Base stats du pokemon actif
        p1_base_stats = p1_active.get("base_stats", {})
        p2_base_stats = p2_active.get("base_stats", {})
        for stat, dataset_stat in zip(["hp", "atk", "def", "spa", "spd", "spe"], ["hp_stat", "atk_stat", "def_stat", "spa_stat", "spd_stat", "spe_stat"]):
            row[f"active_p1_name_{dataset_stat}"] = float(p1_base_stats.get(stat, 0.0))
            row[f"active_p2_name_{dataset_stat}"] = float(p2_base_stats.get(stat, 0.0))
            
        # Matchups types
        p1_types = p1_active.get("types", ["none", "none"])
        p2_types = p2_active.get("types", ["none", "none"])
        row["matchup_p1_type1"] = p1_types[0] if len(p1_types) > 0 else "none"
        row["matchup_p1_type2"] = p1_types[1] if len(p1_types) > 1 else "none"
        row["matchup_p2_type1"] = p2_types[0] if len(p2_types) > 0 else "none"
        row["matchup_p2_type2"] = p2_types[1] if len(p2_types) > 1 else "none"

        # --- 4. Moves (Attaques disponibles) ---
        # Le endpoint renvoie list[MoveModel]
        for i in range(4):
            move_val = moves_data[i].get("id", "none") if i < len(moves_data) else "none"
            row[f"active_p1_move{i+1}"] = move_val
            
        # Attaques de P2 (estimées ou connues via un dictionnaire de l'API s'il existe)
        p2_moves = p2_active.get("moves", [])
        for i in range(4):
            move_val = p2_moves[i] if i < len(p2_moves) else "none"
            row[f"active_p2_move{i+1}"] = move_val

        # --- 5. Aplatissement des équipes (Teams A à F) ---
        letters = ["A", "B", "C", "D", "E", "F"]
        for p, team_key in zip(["p1", "p2"], ["p1", "p2"]):
            team_list = teams_data.get(team_key, [])
            for i, letter in enumerate(letters):
                if i < len(team_list):
                    pkmn = team_list[i]
                    types = pkmn.get("types", ["none", "none"])
                    row[f"pokemon_{p}{letter}"] = pkmn.get("species", "none")
                    row[f"type_1_{p}{letter}"] = types[0] if len(types) > 0 else "none"
                    row[f"type_2_{p}{letter}"] = types[1] if len(types) > 1 else "none"
                    
                    # Gestion du % HP (certains API renvoient un dict, d'autres un float)
                    hp_val = pkmn.get("current_hp_fraction", 0.0) 
                    row[f"hp_{p}{letter}"] = float(hp_val)
                    row[f"status_{p}{letter}"] = pkmn.get("status", "none") or "none"
                else:
                    # Remplissage vide si l'équipe a moins de 6 pokémons
                    row[f"pokemon_{p}{letter}"] = "none"
                    row[f"type_1_{p}{letter}"] = "none"
                    row[f"type_2_{p}{letter}"] = "none"
                    row[f"hp_{p}{letter}"] = 0.0
                    row[f"status_{p}{letter}"] = "none"

        return pd.DataFrame([row])

    def _create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applique les mêmes transformations mathématiques que lors du preprocessing."""
        df["hp_diff"] = df["active_p1_name_hp_stat"] - df["active_p2_name_hp_stat"]
        df["atk_diff"] = df["active_p1_name_atk_stat"] - df["active_p2_name_atk_stat"]
        df["def_diff"] = df["active_p1_name_def_stat"] - df["active_p2_name_def_stat"]
        df["spa_diff"] = df["active_p1_name_spa_stat"] - df["active_p2_name_spa_stat"]
        df["spd_diff"] = df["active_p1_name_spd_stat"] - df["active_p2_name_spd_stat"]
        df["spe_diff"] = df["active_p1_name_spe_stat"] - df["active_p2_name_spe_stat"]

        df["atk_vs_def"] = df["active_p1_name_atk_stat"] - df["active_p2_name_def_stat"]
        df["spa_vs_spd"] = df["active_p1_name_spa_stat"] - df["active_p2_name_spd_stat"]

        df["speed_diff"] = df["active_p1_name_spe_stat"] - df["active_p2_name_spe_stat"]
        df["speed_advantage"] = (df["speed_diff"] > 0).astype(int)

        df["total_stat_p1"] = (
            df["active_p1_name_hp_stat"] + df["active_p1_name_atk_stat"] +
            df["active_p1_name_def_stat"] + df["active_p1_name_spa_stat"] +
            df["active_p1_name_spd_stat"] + df["active_p1_name_spe_stat"]
        )

        df["total_stat_p2"] = (
            df["active_p2_name_hp_stat"] + df["active_p2_name_atk_stat"] +
            df["active_p2_name_def_stat"] + df["active_p2_name_spa_stat"] +
            df["active_p2_name_spd_stat"] + df["active_p2_name_spe_stat"]
        )

        df["total_diff"] = df["total_stat_p1"] - df["total_stat_p2"]
        return df

    def __call__(self) -> str:
        """
        Méthode principale appelée sans arguments : agent()
        Récupère l'état de la partie, génère les features, et prédit l'action.
        """
        # 1. Vérification que l'instance est prête
        ready_res = requests.get(f"{self.base_url}/look/ready", params={"uuid": self.uuid})
        if not ready_res.json():
            return "NOT_READY"

        # 2. Construction du DataFrame initial
        df = self._parse_to_dataframe()

        # 3. Création des features mathématiques
        df = self._create_features(df)

        # =====================================================================
        # 4. SANITIZATION EXTRÊME (Correction de l'erreur string to float)
        # =====================================================================
        # On récupère le pipeline scikit-learn (self.model est ModelWithThreshold, donc .model est le Pipeline)
        pipeline = self.model.model
        preprocessor = pipeline.named_steps["preprocessor"]
        
        # On extrait les listes exactes définies lors de l'entraînement
        cat_cols = preprocessor.transformers_[0][2]
        num_cols = preprocessor.transformers_[1][2]
        
        # On force le format correct pour les colonnes Catégoriques
        for col in cat_cols:
            if col not in df.columns:
                df[col] = "none"
            df[col] = df[col].astype(str)
            
        # On force le format correct pour les colonnes Numériques
        for col in num_cols:
            if col not in df.columns:
                df[col] = 0.0
            # On remplace les "none" par 0.0, et on force la conversion en float
            df[col] = pd.to_numeric(df[col].replace("none", 0.0), errors='coerce').fillna(0.0)
            
        # On s'assure de l'ordre exact et on enlève les colonnes parasites
        expected_columns = list(cat_cols) + list(num_cols)
        df = df[expected_columns]

        # =====================================================================
        # 5. Prédiction
        # =====================================================================
        prediction = self.model.predict(df)[0]
        
        return "SWITCH" if prediction == 1 else "ATTACK"