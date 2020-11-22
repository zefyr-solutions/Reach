window.onload = () => {
    'use strict';
  
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker
        .register('static/sw.js');
        console.log('running main')
    }
  }
