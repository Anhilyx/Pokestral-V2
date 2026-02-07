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
    const selection = ref({
        center: null,
        cornerLngLat: null,
        radius: 100
    });

    // Movement tracking
    const dragOffset = ref({ x: 0, y: 0 });
    const mouseDownPos = ref({ x: 0, y: 0 });
    const isMouseDown = ref(false);

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
        if (interaction === RESIZE_SELECTION) {
            // Compute position
            const center = map.project(selection.value.center);
            const radius = selection.value.radius;
            const distanceX = Math.abs(mousePoint.x - center.x);
            const distanceY = Math.abs(mousePoint.y - center.y);
            const overX = distanceX > radius - HANDLE_RADIUS;
            const overY = distanceY > radius - HANDLE_RADIUS;

            // 3.1. Cursor is in a corner
            if (overX && overY) {
                const rawDx = mousePoint.x - center.x;
                const rawDy = mousePoint.y - center.y;
                canvas.style.cursor = rawDx * rawDy > 0 ?
                                      'nwse-resize' :
                                      'nesw-resize';
            }
            // 3.2. Cursor is on left/right edge
            else if (overX) {
                canvas.style.cursor = 'ew-resize';
            }
            // 3.3. Cursor is on top/bottom edge
            else {
                canvas.style.cursor = 'ns-resize';
            }

            return;
        }

        // 4. No interaction is being performed
        else {
                 if (hovered === MAP
                  && !selection.value.center) canvas.style.cursor = 'crosshair';
            else if (hovered === MAP
                  && selection.value.center)  canvas.style.cursor = 'crosshair';  // or 'grab' to indicate possible interaction
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
    }

    /**
     * Update what is currently hovered
     * @param mousePoint - The current mouse position
     */
    function updateHovered(mousePoint) {
        // If no selection, only the map can be hovered
        if (!selection.value.center) {
            stateHovered.value = MAP;
            return;
        }

        // Retrieve variables for easier access
        const map = mapRef.value;
        const center = map.project(selection.value.center);
        const radius = selection.value.radius;
        const { x: mouseX, y: mouseY } = mousePoint;

        // Corners
             if (Math.abs(mouseX - (center.x - radius)) < HANDLE_RADIUS
              && Math.abs(mouseY - (center.y - radius)) < HANDLE_RADIUS)       stateHovered.value = CORNER_TL;
        else if (Math.abs(mouseX - (center.x + radius)) < HANDLE_RADIUS
              && Math.abs(mouseY - (center.y - radius)) < HANDLE_RADIUS)       stateHovered.value = CORNER_TR;
        else if (Math.abs(mouseX - (center.x - radius)) < HANDLE_RADIUS
              && Math.abs(mouseY - (center.y + radius)) < HANDLE_RADIUS)       stateHovered.value = CORNER_BL;
        else if (Math.abs(mouseX - (center.x + radius)) < HANDLE_RADIUS
              && Math.abs(mouseY - (center.y + radius)) < HANDLE_RADIUS)       stateHovered.value = CORNER_BR;

        // Edges
        else if (Math.abs(mouseX - (center.x - radius)) < BORDER_THICKNESS
              && Math.abs(mouseY - center.y) < radius)                      stateHovered.value = BORDER_L;
        else if (Math.abs(mouseX - (center.x + radius)) < BORDER_THICKNESS
              && Math.abs(mouseY - center.y) < radius)                      stateHovered.value = BORDER_R;
        else if (Math.abs(mouseY - (center.y - radius)) < BORDER_THICKNESS
              && Math.abs(mouseX - center.x) < radius)                      stateHovered.value = BORDER_T;
        else if (Math.abs(mouseY - (center.y + radius)) < BORDER_THICKNESS
              && Math.abs(mouseX - center.x) < radius)                      stateHovered.value = BORDER_B;

        // Selection
        else if (Math.abs(mouseX - center.x) < radius
              && Math.abs(mouseY - center.y) < radius)                      stateHovered.value = SELECTION;

        // Map (default)
        else                                                                stateHovered.value = MAP;
    }

    /**
     * Update the selection geometry and MapLibre source.
     * @param emitRequested - Whether to emit the 'area-changed' event after updating
     */
    function updateMap(emitRequested = false) {
        // Skip if map or selection is not ready
        if (!mapRef.value || !selection.value.center) return;

        // Retrieve variables for easier access
        const map = mapRef.value;
        const source = map.getSource(SRC_ID);
        const center = selection.value.center;
        const radius = selection.value.radius;

        // Skip if source layer is missing
        if (!source) return;

        // 1. Calculate Geometry (Pixels -> LngLat)
        const centerPx = map.project(center);
       
        // Calculate the 4 corners in absolute pixels
        const pxCoords = [
            { x: centerPx.x - radius, y: centerPx.y - radius }, // TL
            { x: centerPx.x + radius, y: centerPx.y - radius }, // TR
            { x: centerPx.x + radius, y: centerPx.y + radius }, // BR
            { x: centerPx.x - radius, y: centerPx.y + radius }  // BL
        ];

        // Convert back to GPS coordinates (LngLat)
        const polyCoords = pxCoords.map(p => {
            const ll = map.unproject([p.x, p.y]);
            return [ll.lng, ll.lat];
        });
       
        // Close the polygon loop
        polyCoords.push(polyCoords[0]);

        // Create features for handles (corners)
        const cornerFeatures = pxCoords.map(p => {
            const ll = map.unproject([p.x, p.y]);
            return {
                type: 'Feature',
                geometry: { type: 'Point', coordinates: [ll.lng, ll.lat] },
                properties: { type: 'corner' }
            };
        });

        // 2. Update Zoom Reference
        // Save the precise GPS position of a corner to recalculate radius on zoom
        selection.value.cornerLngLat = map.unproject([
            centerPx.x - radius,
            centerPx.y - radius
        ]);

        // 3. Update MapLibre Source
        source.setData({
            type: 'FeatureCollection',
            features: [
                {
                    type: 'Feature',
                    geometry: { type: 'Polygon', coordinates: [polyCoords] },
                    properties: { type: 'area' }
                },
                ...cornerFeatures
            ]
        });

        // 4. Emit to parent if requested
        if (emitRequested) {
            emit('area-changed', {
                center: center,
                coordinates: polyCoords,
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
       
        // Update values (1)
        mouseDownPos.value = mouse;
        isMouseDown.value = true;
        updateHovered(mouse);

        // Determine interaction type
             if ((stateHovered.value & 0xF0) == BORDER
              || (stateHovered.value & 0xF0) == CORNER)  stateInteraction.value = RESIZE_SELECTION;
        else if (stateHovered.value === SELECTION)       stateInteraction.value = MOVE_SELECTION;
        else                                             stateInteraction.value = PRE_MOVE_MAP;

        // Prepare interaction
        if (
            stateInteraction.value === RESIZE_SELECTION ||
            stateInteraction.value === MOVE_SELECTION
        ) {
            // Disable original map events
            event.preventDefault();
            map.dragPan.disable();

            // Register drag offset for move interaction
            if (stateInteraction.value === MOVE_SELECTION) {
                const center = map.project(selection.value.center);
                dragOffset.value = {
                    x: center.x - mouse.x,
                    y: center.y - mouse.y
                };
            }
        }

        // Update values (2)
        updateCursor(mouse);
    };

    function onMouseMove(event) {
        // Skip if map is not ready
        if (!mapRef.value) return;

        // Retrieve variables for easier access
        const map = mapRef.value;
        const mouse = event.point;

        // Resize selection
        if (stateInteraction.value === RESIZE_SELECTION) {
            const center = map.project(selection.value.center);
            const distanceX = Math.abs(mouse.x - center.x);
            const distanceY = Math.abs(mouse.y - center.y);
            const newRadius = Math.max(distanceX, distanceY);
            selection.value.radius = Math.max(newRadius, 20);
            updateMap();
        }

        // Move selection
        else if (stateInteraction.value === MOVE_SELECTION) {
            const newCenter = {
                x: mouse.x + dragOffset.value.x,
                y: mouse.y + dragOffset.value.y
            };
            selection.value.center = map.unproject(newCenter);
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
            selection.value.center = event.lngLat;
            selection.value.radius = 100;
            updateMap();
        }

        // Emit event if selection was created/modified
        if (
            stateInteraction.value === PRE_MOVE_MAP ||
            stateInteraction.value === MOVE_SELECTION ||
            stateInteraction.value === RESIZE_SELECTION
        ) {
            updateMap(true);
        }

        // Update/reset values
        isMouseDown.value = false;
        stateInteraction.value = IDLE;
        map.dragPan.enable();
        updateHovered(mouse);
        updateCursor(mouse);
    };

    function onZoom() {
        // Skip if map is not ready or no selection
        if (
            !selection.value.center ||
            !mapRef.value
        ) return;
       
        // Retrieve variables for easier access
        const map = mapRef.value;

        // Compute radius in pixels based on the distance between the center and corner
        const centerPx = map.project(selection.value.center);
        const cornerPx = map.project(selection.value.cornerLngLat);

        // Update radius
        selection.value.radius = Math.abs(centerPx.x - cornerPx.x);
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
        mapObject.on('zoom', onZoom);
    };
</script>

<template>
    <div class="holo-street-map-plus">
        <HoloStreetMap @load="onMapReady" />
    </div>
</template>