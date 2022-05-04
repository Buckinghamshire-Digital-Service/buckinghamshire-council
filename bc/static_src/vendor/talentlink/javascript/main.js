/* eslint-disable */
(function($){
    function onError() {
        hidePreloader();
        var $tpl = $('.apply-application-network-error-content').show().detach();
        $('[data-lumesse-apply-container]').append($tpl);
    }

    function onLoad() {
        hidePreloader();
    }

    function hidePreloader() {
        $('.apply-preloader').remove();
    }

    function hideMenuOnSubmit() {
        $('#apply-nav').remove();
        $('#apply-content').removeClass('col-lg-offset-3 col-sm-offset-4 col-sm-7');
        $('[data-apply-content]').append(
            createBeacon('https://beacon.adcourier.com/98392bd3-9df8-43fb-83aa-b1ec77c6f7bd.gif?type=confirm')
        );
    }

    function widgetsLoaded() {
        return typeof lumesse != 'undefined' || (require && require.specified && require.specified("ApplyInitializer"));
    }

    function widgetsNamespaced() {
        return typeof lumesse != 'undefined' && 'require' in lumesse;
    }

    function createBeacon(url) {
        const img = document.createElement('img');
        img.src = url;
        return img;
    }

    $(document).ready(function () {
        if (!widgetsLoaded()) {
            onError();
        } else {
            // add tracking beacon here
            $('[data-apply-content]').append(
                createBeacon('https://beacon.adcourier.com/98392bd3-9df8-43fb-83aa-b1ec77c6f7bd.gif?type=apply')
            );
            var requireFunction = widgetsNamespaced() ? lumesse.require : require;
            requireFunction([
                "jquery-noConflict",
                "underscore-noConflict",
                "backbone-noConflict",
                "ApplyCustomerEvents",
                "ApplyInitializer",
                "ApplicationFormTemplates"
            ], function ($, _, Backbone, ApplyCustomerEvents, ApplyInitializer, ApplicationFormTemplates) {
                ApplyCustomerEvents.once(ApplyCustomerEvents.componentLoadingFailed, onError);
                ApplyCustomerEvents.once(ApplyCustomerEvents.appInitialized, onLoad);
                ApplyCustomerEvents.once(ApplyCustomerEvents.submissionAccepted, hideMenuOnSubmit);

                (function(){
                    var templatesCount = 0;
                    var templatesLoaded = -1;

                    $('script').each(function () {
                        if ($(this).attr('type') === 'text/template') {
                            loadTemplate($(this).data('template'), $(this).attr('src'));
                        }
                    });

                    function loadTemplate(templateName, templateUrl) {
                        templatesCount++;

                        $.get(templateUrl, function (source) {
                            ApplicationFormTemplates.set(templateName, source);
                        }).always(templateLoadCompleted);
                    }

                    function templateLoadCompleted() {
                        templatesLoaded++;

                        if (templatesLoaded === templatesCount) {
                            ApplyInitializer.bind();
                        }
                    }

                    // call this function in case there are no templates
                    templateLoadCompleted();
                })();
            });
        }
    });
})(jQuery);
