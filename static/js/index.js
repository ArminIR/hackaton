import { queryEl, hideEl, showEl, resetEl } from "./helpers.js";
import { switchViewTo } from "./views.js";
import app from "./model/index.js";

// Buttons
const [
    // Start view Button
    startBtn,
    // Main view Button
    mainBtn,
    // Open Settings Button
    settingsBtn,
    // Close Settings Button
    closeBtn
] = ['#startBtn', '#mainBtn', '#settBtn', '#closeBtn'].map(id => queryEl(id));

// Track the view state
let isSettingsViewOpen = false;

// Show Intro with Help
startBtn.addEventListener('click', function () {
   // help & settings
   switchViewTo('help');
});

// Main View
mainBtn.addEventListener('click', function () {
    // Using Speech
    switchViewTo('main');
});

// Settings View
settingsBtn.addEventListener('click', function () {
    // Open settings view
    switchViewTo('open-settings');
    // Hide the settings button
    hideEl(settingsBtn);
    // Mark settings view as open
    isSettingsViewOpen = true;
});

// Hide Settings View
closeBtn.addEventListener('click', function () {
    // Close settings view
    switchViewTo('close-settings');

    // Reset the settings button display
    resetEl(settingsBtn);

    // Mark settings view as closed
    isSettingsViewOpen = false;
});

// When Everything is loaded
window.addEventListener('DOMContentLoaded', function () {
    // Hide loader & switch to start
    switchViewTo('start');
    // Check for error
    if (app.synth == null || app.synth == 'undefined') {
        // Go to Error page
        switchViewTo('error');
    } else {
        // Fetch Voices
        app.work();
    }

    // Clear input
    app.textBlock.value = '';
}, false);