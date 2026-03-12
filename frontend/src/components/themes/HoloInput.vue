<template>
    <HoloTheme class="holo-input">
        <slot></slot>
    </HoloTheme>
</template>

<style scoped>
    /* Variables */
    .holo-input {
        /* Layout */
        --holo-input__label-height: 16px;

        /* Background */
        --holo-input__background-color: color-mix(in srgb, var(--holo-theme__background-color), transparent 92.5%);
        --holo-input__background: var(--holo-input__background-color);
       
        --holo-input__background-color-hover: color-mix(in srgb, var(--holo-theme__background-color), transparent 90%);
        --holo-input__background-hover: var(--holo-input__background-color-hover);
       
        --holo-input__background-color-focus: color-mix(in srgb, var(--holo-theme__background-color), transparent 85%);
        --holo-input__background-focus: var(--holo-input__background-color-focus);

        /* Glow */
        --holo-input__glow-color: color-mix(in srgb, var(--holo-theme__glow-medium-color), transparent 50%);
        --holo-input__glow: 0 0 var(--holo-theme__glow-strength-low) var(--holo-input__glow-color);
       
        --holo-input__glow-color-hover: color-mix(in srgb, var(--holo-theme__glow-medium-color), transparent 40%);
        --holo-input__glow-hover: 0 0 var(--holo-theme__glow-strength-medium) var(--holo-input__glow-color-hover);
       
        --holo-input__glow-color-focus: color-mix(in srgb, var(--holo-theme__glow-medium-color), transparent 30%);
        --holo-input__glow-focus: 0 0 var(--holo-theme__glow-strength-high) var(--holo-input__glow-color-focus);

        /* Colors 2 */
        --holo-input__empty-color-2: color-mix(in srgb, var(--holo-theme__background-color-off), transparent                          70%);
        --holo-input__fill-color-2:  color-mix(in srgb, var(--holo-theme__background-color),     transparent                          50%);
        --holo-input__thumb-color-2: color-mix(in srgb, var(--holo-theme__background-color),     var(--holo-theme__glow-medium-color) 20%);
       
        --holo-input__empty-color-2-hover: color-mix(in srgb, var(--holo-theme__background-color-off), transparent                          70%);
        --holo-input__fill-color-2-hover:  color-mix(in srgb, var(--holo-theme__background-color),     transparent                          30%);
        --holo-input__thumb-color-2-hover: color-mix(in srgb, var(--holo-theme__background-color),     var(--holo-theme__glow-medium-color) 35%);
       
        --holo-input__empty-color-2-focus: color-mix(in srgb, var(--holo-theme__background-color-off), transparent                           70%);
        --holo-input__fill-color-2-focus:  color-mix(in srgb, var(--holo-theme__background-color),     transparent                           10%);
        --holo-input__thumb-color-2-focus: color-mix(in srgb, var(--holo-theme__background-color),     var(--holo-theme__glow-medium-color) 100%);

        /* Glow */
        --holo-input__empty-glow-2: 0 0 0px                                                                                    var(--holo-input__empty-color-2);
        --holo-input__fill-glow-2:  0 0 var(--holo-theme__glow-strength-low)                                                   var(--holo-input__glow-color-2);
        --holo-input__thumb-glow-2: 0 0 calc(var(--holo-theme__glow-strength-low) * var(--holo-input__thumb-glow-multiplier)) var(--holo-input__glow-color-2);

        --holo-input__empty-glow-2-hover: 0 0 0px                                                                                      var(--holo-input__empty-color-2);
        --holo-input__fill-glow-2-hover:  0 0 var(--holo-theme__glow-strength-medium)                                                   var(--holo-input__glow-color-2);
        --holo-input__thumb-glow-2-hover: 0 0 calc(var(--holo-theme__glow-strength-medium) * var(--holo-input__thumb-glow-multiplier)) var(--holo-input__glow-color-2);

        --holo-input__empty-glow-2-focus: 0 0 0px                                                                                     var(--holo-input__empty-color-2);
        --holo-input__fill-glow-2-focus:  0 0 var(--holo-theme__glow-strength-high)                                                   var(--holo-input__glow-color-2);
        --holo-input__thumb-glow-2-focus: 0 0 calc(var(--holo-theme__glow-strength-high) * var(--holo-input__thumb-glow-multiplier)) var(--holo-input__glow-color-2);
    }
</style>