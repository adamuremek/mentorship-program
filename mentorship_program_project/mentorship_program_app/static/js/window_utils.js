// window_utils.js

// Disable the window scroll
export function disableScroll() {
    // Store the current scroll position
    window.scrollPosition = window.scrollY;

    // Lock the scroll position
    document.body.style = 'hidden';
    document.body.style.position = 'fixed';
    document.body.style.top = `-${window.scrollPosition}px`;
    document.body.style.width = '100%';

    // Prevent scrolling on touch devices
    window.addEventListener('touchmove', preventTouchMove, { passive: false });
}

// Enable the system scroll
export function enableScroll() {
    document.body.style.removeProperty('overflow');
    document.body.style.removeProperty('position');
    document.body.style.removeProperty('top');
    document.body.style.removeProperty('width');
    // Restore the scroll position
    window.scrollTo(0, window.scrollPosition)

    // Re-enable scrolling on touch devices
    window.removeEventListener('touchmove', preventTouchMove, { passive: false });
}

// Clear the text of the input field
export function clearThis(target) {
    target.value = "";
}

// Helper function to prevent touchmove event
function preventTouchMove(event) {
    event.preventDefault();
}