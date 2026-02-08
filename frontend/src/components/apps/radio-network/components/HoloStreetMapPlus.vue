<script setup>
    import { ref, shallowRef } from 'vue';

    const emit = defineEmits([
        'area-changed'
    ]);

    /************
    | Variables |
    ************/

    // Map elements
    const mapRef = shallowRef(null);
   
    // CHANGED: Using bounds (SW/NE) instead of center/radius to allow asymmetric resizing
    const selection = ref({
        bounds: null, // { sw: LngLat, ne: LngLat }
        isMoving: false
    });

    // Movement tracking
    const dragStartMousePos = ref({ x: 0, y: 0 });
    const dragStartBounds = ref(null); // Stores bounds state at start of drag

    // Map layers
    const SRC_ID = 'selection-source';
    const LAYER_FILL = 'selection-layer-fill';
    const LAYER_LINE = 'selection-layer-line';
    const LAYER_CORNERS = 'selection-layer-corners';

    // Interaction state
    const IDLE             = 0x00;
    const MOVE_MAP         = 0x10;
    const PRE_MOVE_MAP     = 0x11;
    const MOVE_SELECTION   = 0x20;
    const RESIZE_SELECTION = 0x30;
    const RESIZE_N         = 0x31;
    const RESIZE_E         = 0x32;
    const RESIZE_S         = 0x33;
    const RESIZE_W         = 0x34;
    const RESIZE_NE        = 0x35;
    const RESIZE_NW        = 0x36;
    const RESIZE_SE        = 0x37;
    const RESIZE_SW        = 0x38;
    const stateInteraction = ref(IDLE);

    // Hovered state
    const MAP       = 0x00;
    const SELECTION = 0x10;
    const BORDER    = 0x20;
    const BORDER_T  = 0X21;
    const BORDER_B  = 0x22;
    const BORDER_L  = 0x23;
    const BORDER_R  = 0x24;
    const CORNER    = 0x30;
    const CORNER_TL = 0x31;
    const CORNER_TR = 0x32;
    const CORNER_BL = 0x33;
    const CORNER_BR = 0x34;
    const stateHovered = ref(MAP);

    // Visual
    const BACKGROUND_COLOR = '#bbb';
    const BACKGROUND_OPACITY = 0.2;
    const BORDER_COLOR = '#fff';
    const BORDER_THICKNESS = 2;
    const HANDLE_COLOR = '#444';
    const HANDLE_RADIUS = 5;

    /************
    | Functions |
    ************/

    /**
     * Helper to get pixel coordinates of current bounds
     */
    function getSelectionPixels(map) {
        if (!selection.value.bounds) return null;
       
        const sw = map.project(selection.value.bounds.sw);
        const ne = map.project(selection.value.bounds.ne);

        return {
            left: Math.min(sw.x, ne.x),
            right: Math.max(sw.x, ne.x),
            top: Math.min(sw.y, ne.y),
            bottom: Math.max(sw.y, ne.y)
        };
    }

    /**
     * Update the cursor style based on the current states.
     * @param mousePoint - The current mouse position
     */
    function updateCursor(mousePoint) {
        // Skip if map is not ready
        if (!mapRef.value) return;

        // Retrieve variables for easier access
        const map = mapRef.value;
        const canvas = map.getCanvas();
        const interaction = stateInteraction.value;
        const hovered = stateHovered.value;

        // 1. The map is being dragged
        if (interaction === MOVE_MAP) {
            canvas.style.cursor = 'grabbing';
            return;
        }

        // 2. The selection is being moved
        if (interaction === MOVE_SELECTION) {
            canvas.style.cursor = 'move';
            return;
        }

        // 3. The selection is being resized
        if ((interaction & 0xF0) === RESIZE_SELECTION) {
                 if (interaction === RESIZE_N
                  || interaction === RESIZE_S)   canvas.style.cursor = 'ns-resize';
            else if (interaction === RESIZE_E
                 ||  interaction === RESIZE_W)   canvas.style.cursor = 'ew-resize';
            else if (interaction === RESIZE_NE
                  || interaction === RESIZE_SW)  canvas.style.cursor = 'nesw-resize';
            else if (interaction === RESIZE_NW
                  || interaction === RESIZE_SE)  canvas.style.cursor = 'nwse-resize';
           
            return;
        }

        // 4. No interaction is being performed
             if (hovered === MAP
             && !selection.value.bounds) canvas.style.cursor = 'crosshair';
        else if (hovered === MAP
              && selection.value.bounds)  canvas.style.cursor = 'crosshair';
        else if (hovered === SELECTION)   canvas.style.cursor = 'move';
        else if (hovered === BORDER_T
              || hovered === BORDER_B)    canvas.style.cursor = 'ns-resize';
        else if (hovered === BORDER_L
              || hovered === BORDER_R)    canvas.style.cursor = 'ew-resize';
        else if (hovered === CORNER_TL
              || hovered === CORNER_BR)   canvas.style.cursor = 'nwse-resize';
        else if (hovered === CORNER_TR
              || hovered === CORNER_BL)   canvas.style.cursor = 'nesw-resize';
        else                              canvas.style.cursor = '';
    }

    /**
     * Update what is currently hovered
     * @param mousePoint - The current mouse position
     */
    function updateHovered(mousePoint) {
        // If no selection, only the map can be hovered
        if (!selection.value.bounds) {
            stateHovered.value = MAP;
            return;
        }

        // Retrieve variables for easier access
        const map = mapRef.value;
        const px = getSelectionPixels(map);
        const { x: mouseX, y: mouseY } = mousePoint;

        // Tolerances
        const hr = HANDLE_RADIUS * 1.5; // Hitbox slightly larger for handles
        const br = BORDER_THICKNESS + 5; // Hitbox for border

        // Corners
             if (Math.abs(mouseX - px.left) < hr
              && Math.abs(mouseY - px.top) < hr)       stateHovered.value = CORNER_TL;
        else if (Math.abs(mouseX - px.right) < hr
              && Math.abs(mouseY - px.top) < hr)       stateHovered.value = CORNER_TR;
        else if (Math.abs(mouseX - px.left) < hr
              && Math.abs(mouseY - px.bottom) < hr)    stateHovered.value = CORNER_BL;
        else if (Math.abs(mouseX - px.right) < hr
              && Math.abs(mouseY - px.bottom) < hr)    stateHovered.value = CORNER_BR;

        // Edges
        else if (Math.abs(mouseX - px.left) < br
              && mouseY > px.top && mouseY < px.bottom)     stateHovered.value = BORDER_L;
        else if (Math.abs(mouseX - px.right) < br
              && mouseY > px.top && mouseY < px.bottom)     stateHovered.value = BORDER_R;
        else if (Math.abs(mouseY - px.top) < br
              && mouseX > px.left && mouseX < px.right)     stateHovered.value = BORDER_T;
        else if (Math.abs(mouseY - px.bottom) < br
              && mouseX > px.left && mouseX < px.right)     stateHovered.value = BORDER_B;

        // Selection body
        else if (mouseX > px.left && mouseX < px.right
              && mouseY > px.top && mouseY < px.bottom)     stateHovered.value = SELECTION;

        // Map (default)
        else                                                stateHovered.value = MAP;
    }

    /**
     * Update the selection geometry and MapLibre source.
     * @param emitRequested - Whether to emit the 'area-changed' event after updating
     */
    function updateMap(emitRequested = false) {
        // Skip if map or selection is not ready
        if (!mapRef.value || !selection.value.bounds) return;

        // Retrieve variables for easier access
        const map = mapRef.value;
        const source = map.getSource(SRC_ID);
       
        // Skip if source layer is missing
        if (!source) return;

        // 1. Calculate Geometry
        // We use bounds to determine coordinates
        const { sw, ne } = selection.value.bounds;
       
        // Create polygon coordinates (CCW)
        const polyCoords = [[
            [sw.lng, ne.lat], // TL
            [ne.lng, ne.lat], // TR
            [ne.lng, sw.lat], // BR
            [sw.lng, sw.lat], // BL
            [sw.lng, ne.lat]  // Close loop
        ]];

        // Create features for handles (corners)
        const cornerPoints = [
            [sw.lng, ne.lat], // TL
            [ne.lng, ne.lat], // TR
            [ne.lng, sw.lat], // BR
            [sw.lng, sw.lat]  // BL
        ];

        const cornerFeatures = cornerPoints.map(coord => {
            return {
                type: 'Feature',
                geometry: { type: 'Point', coordinates: coord },
                properties: { type: 'corner' }
            };
        });

        // 2. Update MapLibre Source
        source.setData({
            type: 'FeatureCollection',
            features: [
                {
                    type: 'Feature',
                    geometry: { type: 'Polygon', coordinates: polyCoords },
                    properties: { type: 'area' }
                },
                ...cornerFeatures
            ]
        });

        // 3. Emit to parent if requested
        if (emitRequested) {
            // Calculate an approximate pixel radius for compatibility
            const centerLng = (sw.lng + ne.lng) / 2;
            const centerLat = (sw.lat + ne.lat) / 2;
            const centerPx = map.project([centerLng, centerLat]);
            const cornerPx = map.project([ne.lng, ne.lat]);
            const radius = Math.hypot(centerPx.x - cornerPx.x, centerPx.y - cornerPx.y);

            emit('area-changed', {
                center: { lng: centerLng, lat: centerLat },
                coordinates: {
                    minLng: sw.lng,
                    minLat: sw.lat,
                    maxLng: ne.lng,
                    maxLat: ne.lat
                },
                pixelRadius: radius
            });
        }
    }

    /*********
    | Events |
    *********/

    function onMouseDown(event) {
        // Skip if map is not ready
        if (!mapRef.value) return;

        // Retrieve variables for easier access
        const map = mapRef.value;
        const mouse = event.point;
      
        // Update values
        updateHovered(mouse);

        // Determine interaction type
             if (stateHovered.value === BORDER_T)   stateInteraction.value = RESIZE_N;
        else if (stateHovered.value === BORDER_B)   stateInteraction.value = RESIZE_S;
        else if (stateHovered.value === BORDER_L)   stateInteraction.value = RESIZE_W;
        else if (stateHovered.value === BORDER_R)   stateInteraction.value = RESIZE_E;
        else if (stateHovered.value === CORNER_TL)  stateInteraction.value = RESIZE_NW;
        else if (stateHovered.value === CORNER_TR)  stateInteraction.value = RESIZE_NE;
        else if (stateHovered.value === CORNER_BL)  stateInteraction.value = RESIZE_SW;
        else if (stateHovered.value === CORNER_BR)  stateInteraction.value = RESIZE_SE;
        else if (stateHovered.value === SELECTION)  stateInteraction.value = MOVE_SELECTION;
        else                                        stateInteraction.value = PRE_MOVE_MAP;

        // Store initial positions for drag calculations
        dragStartMousePos.value = mouse;
        if (selection.value.bounds) {
            // Clone the bounds object to avoid reference issues
            dragStartBounds.value = {
                sw: { ...selection.value.bounds.sw },
                ne: { ...selection.value.bounds.ne }
            };
        }

        // Prepare interaction
        if (
            (stateInteraction.value & 0xF0) === RESIZE_SELECTION ||
            stateInteraction.value === MOVE_SELECTION
        ) {
            // Disable original map events
            event.preventDefault();
            map.dragPan.disable();
        }

        // Update cursor immediately
        updateCursor(mouse);
    };

    function onMouseMove(event) {
        // Skip if map is not ready
        if (!mapRef.value) return;

        // Retrieve variables for easier access
        const map = mapRef.value;
        const mouse = event.point;

        // Resize selection
        if ((stateInteraction.value & 0xF0) === RESIZE_SELECTION) {
            // Get original bounds in pixels
            const startSW = map.project(dragStartBounds.value.sw);
            const startNE = map.project(dragStartBounds.value.ne);

            // Establish current box edges in pixels
            // Note: MapLibre Y coordinates increase downwards
            let top = Math.min(startSW.y, startNE.y);
            let bottom = Math.max(startSW.y, startNE.y);
            let left = Math.min(startSW.x, startNE.x);
            let right = Math.max(startSW.x, startNE.x);

            // Apply modifications based on the active handle
            // Only the side being dragged is updated, others remain fixed
            if (stateInteraction.value === RESIZE_N  || stateInteraction.value === RESIZE_NW || stateInteraction.value === RESIZE_NE) {
                top = mouse.y;
            }
            if (stateInteraction.value === RESIZE_S  || stateInteraction.value === RESIZE_SW || stateInteraction.value === RESIZE_SE) {
                bottom = mouse.y;
            }
            if (stateInteraction.value === RESIZE_W  || stateInteraction.value === RESIZE_NW || stateInteraction.value === RESIZE_SW) {
                left = mouse.x;
            }
            if (stateInteraction.value === RESIZE_E  || stateInteraction.value === RESIZE_NE || stateInteraction.value === RESIZE_SE) {
                right = mouse.x;
            }

            // Safety: Ensure minimum size (10px)
            if (right - left < 10) {
                 if (stateInteraction.value === RESIZE_E || stateInteraction.value === RESIZE_NE || stateInteraction.value === RESIZE_SE) right = left + 10;
                 else left = right - 10;
            }
            if (bottom - top < 10) {
                if (stateInteraction.value === RESIZE_S || stateInteraction.value === RESIZE_SW || stateInteraction.value === RESIZE_SE) bottom = top + 10;
                else top = bottom - 10;
            }

            // Convert back to LngLat
            const newSW = map.unproject([left, bottom]); // Bottom-Left pixel is SW
            const newNE = map.unproject([right, top]);   // Top-Right pixel is NE

            selection.value.bounds = {
                sw: newSW,
                ne: newNE
            };
           
            updateMap();
        }

        // Move selection
        else if (stateInteraction.value === MOVE_SELECTION) {
            // Calculate delta in pixels
            const dx = mouse.x - dragStartMousePos.value.x;
            const dy = mouse.y - dragStartMousePos.value.y;

            // Project start bounds to pixels
            const pSW = map.project(dragStartBounds.value.sw);
            const pNE = map.project(dragStartBounds.value.ne);

            // Apply delta
            const newPSW = { x: pSW.x + dx, y: pSW.y + dy };
            const newPNE = { x: pNE.x + dx, y: pNE.y + dy };

            // Unproject back
            selection.value.bounds = {
                sw: map.unproject(newPSW),
                ne: map.unproject(newPNE)
            };
           
            updateMap();
        }

        // Update values
        updateHovered(mouse);
        updateCursor(mouse);
    };

    function onMapDrag(event) {
        // Skip if map is not ready
        if (!mapRef.value) return;

        // Retrieve variables for easier access
        const map = mapRef.value;
        const mouse = {
            x: event.originalEvent.x - map.getCanvas().getBoundingClientRect().left,
            y: event.originalEvent.y - map.getCanvas().getBoundingClientRect().top
        };

        // Start dragging the map if the mouse has moved
        if (stateInteraction.value === PRE_MOVE_MAP) {
            stateInteraction.value = MOVE_MAP;
        }

        // Update values
        updateHovered(mouse);
        updateCursor(mouse);
    };

    function onMouseUp(event) {
        // Skip if map is not ready
        if (!mapRef.value) return;

        // Retrieve variables for easier access
        const map = mapRef.value;
        const mouse = event.point;

        // Create selection if a click (without movement) was performed on the map
        if (stateInteraction.value === PRE_MOVE_MAP) {
            // Create a default box around the click point
            const radius = 100; // pixels
            const center = map.project(event.lngLat);
            
            const sw = map.unproject([center.x - radius, center.y + radius]);
            const ne = map.unproject([center.x + radius, center.y - radius]);

            selection.value.bounds = { sw, ne };
            updateMap();
        }

        // Emit event if selection was created/modified
        if (
            stateInteraction.value === PRE_MOVE_MAP ||
            stateInteraction.value === MOVE_SELECTION ||
            (stateInteraction.value & 0xF0) === RESIZE_SELECTION
        ) {
            updateMap(true);
        }

        // Update/reset values
        stateInteraction.value = IDLE;
        dragStartBounds.value = null;
        map.dragPan.enable();
        updateHovered(mouse);
        updateCursor(mouse);
    };

    /*************
    | Create map |
    *************/

    function initLayers() {
        // Skip if map is not ready or layers already exist
        const map = mapRef.value;
        if (!map || map.getSource(SRC_ID)) return;

        // Create source
        map.addSource(SRC_ID, { type: 'geojson', data: { type: 'FeatureCollection', features: [] } });

        // Create background fill
        map.addLayer({
            id: LAYER_FILL,
            type: 'fill',
            source: SRC_ID,
            filter: ['==', '$type', 'Polygon'],
            paint: {
                'fill-color': BACKGROUND_COLOR,
                'fill-opacity': BACKGROUND_OPACITY
            }
        });

        // Create dashed border
        map.addLayer({
            id: LAYER_LINE,
            type: 'line',
            source: SRC_ID,
            filter: ['==', '$type', 'Polygon'],
            paint: {
                'line-color': BORDER_COLOR,
                'line-width': BORDER_THICKNESS,
                'line-dasharray': [2, 2],
            }
        });

        // Create corner handles
        map.addLayer({
            id: LAYER_CORNERS,
            type: 'circle',
            source: SRC_ID,
            filter: ['==', '$type', 'Point'],
            paint: {
                'circle-radius': HANDLE_RADIUS,
                'circle-color': HANDLE_COLOR,
                'circle-stroke-width': BORDER_THICKNESS,
                'circle-stroke-color': BORDER_COLOR
            }
        });
    };

    // Initialize map on load
    function onMapReady(mapObject) {
        // Retrieve variables for easier access
        mapRef.value = mapObject;

        // Initialize layers
        initLayers();

        // Register events
        mapObject.on('mousedown', onMouseDown);
        mapObject.on('mousemove', onMouseMove);
        mapObject.on('drag', onMapDrag);
        mapObject.on('mouseup', onMouseUp);
    };
</script>

<template>
    <div class="holo-street-map-plus">
        <HoloStreetMap @load="onMapReady" />
    </div>
</template>