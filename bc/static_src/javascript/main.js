import '@babel/polyfill';
import React from 'react';
import ReactDOM from 'react-dom';
import TestReact from './components/TestReact';
import MobileMenu from './components/mobile-menu';
import MobileSubMenu from './components/mobile-sub-menu';
import CookieWarning from './components/cookie-message';
import Accordion from './components/accordion';
import AreaSearchForm from './components/area-search-form';
import Carousel from './components/carousel';
import ConditionalField from './components/conditional-field';
import HeightEqualizer from './components/height-equalizer';
import ProgressBar from './components/progress-bar';
import ToggleTarget from './components/toggle-target';
import VideoModal from './components/video-modal';
import FormSubmit from './components/form-submit';
import Filters from './components/job-filters';
import FeedbackWidget from './components/feedback-widget';
import Chart from './components/chart';
import GoogleMap from './components/map';

// Add polyfill fix for forEach carousel
import foreachPolyfill from './polyfills/foreach-polyfill';
// Add polyfill fix for closest() method in conditional fields
import closestPolyfill from './polyfills/closest-polyfill';
import 'whatwg-fetch';

import '../sass/main.scss';

foreachPolyfill();
closestPolyfill();

// Open the mobile menu callback
function openMobileMenu() {
    document.querySelector('body').classList.add('no-scroll');
    document.querySelector('[data-mobile-menu]').classList.add('is-visible');
}

// Close the mobile menu callback.
function closeMobileMenu() {
    document.querySelector('body').classList.remove('no-scroll');
    document.querySelector('[data-mobile-menu]').classList.remove('is-visible');
}

document.addEventListener('DOMContentLoaded', () => {
    /* eslint-disable no-restricted-syntax, no-new */
    const cookie = document.querySelector(CookieWarning.selector());
    new CookieWarning(cookie);

    for (const accordion of document.querySelectorAll(Accordion.selector())) {
        new Accordion(accordion);
    }

    for (const areasearchform of document.querySelectorAll(
        AreaSearchForm.selector(),
    )) {
        new AreaSearchForm(areasearchform);
    }

    for (const carousel of document.querySelectorAll(Carousel.selector())) {
        new Carousel(carousel);
    }

    for (const conditionalfield of document.querySelectorAll(
        ConditionalField.selector(),
    )) {
        new ConditionalField(conditionalfield);
    }

    for (const formsubmit of document.querySelectorAll(FormSubmit.selector())) {
        new FormSubmit(formsubmit);
    }

    for (const filters of document.querySelectorAll(Filters.selector())) {
        new Filters(filters);
    }

    for (const heightEqualizer of document.querySelectorAll(
        HeightEqualizer.selector(),
    )) {
        new HeightEqualizer(heightEqualizer);
    }

    for (const mobilemenu of document.querySelectorAll(MobileMenu.selector())) {
        new MobileMenu(mobilemenu, openMobileMenu, closeMobileMenu);
    }

    for (const mobilesubmenu of document.querySelectorAll(
        MobileSubMenu.selector(),
    )) {
        new MobileSubMenu(mobilesubmenu);
    }

    // Toggle subnav visibility
    for (const subnavBack of document.querySelectorAll('[data-subnav-back]')) {
        subnavBack.addEventListener('click', () => {
            subnavBack.parentNode.classList.remove('is-visible');
        });
    }

    for (const progressbar of document.querySelectorAll(
        ProgressBar.selector(),
    )) {
        new ProgressBar(progressbar);
    }

    for (const toggleTarget of document.querySelectorAll(
        ToggleTarget.selector(),
    )) {
        new ToggleTarget(toggleTarget);
    }

    for (const videomodal of document.querySelectorAll(VideoModal.selector())) {
        new VideoModal(videomodal);
    }

    for (const feedbackwidget of document.querySelectorAll(
        FeedbackWidget.selector(),
    )) {
        new FeedbackWidget(feedbackwidget);
    }

    for (const chart of document.querySelectorAll(Chart.selector())) {
        new Chart(chart);
    }

    for (const googlemap of document.querySelectorAll(GoogleMap.selector())) {
        new GoogleMap(googlemap);
    }

    // Test react - add a div with a data attribute of `data-test-react` to test
    for (const element of document.querySelectorAll('[data-test-react]')) {
        ReactDOM.render(<TestReact greeting="boo!" />, element);
    }
});
