Utils = {};

(function (Utils) {

    Utils.getRendered = function(selector, data) {
        var template_element = $(selector);
        var parent = template_element.data('parent');
        var html = _.template(template_element.html())(data);
        if (parent)
            return $(parent).html(html);
        return html;
    };

    Utils.postJSON = function(options) {
        if (!options.type) options.type = 'POST';
        if (options.data) options.data = JSON.stringify(options.data);
        if (!options.contentType) options.contentType = 'application/json';
        $.ajax(options);
    };

    Utils.disableButton = function(button, hideSpinner) {
        button.addClass('btn-disabled');
        if (!hideSpinner) button.addClass('btn-disabled-spinner')
    }

    Utils.enableButton = function(button) {
        button.removeClass('btn-disabled btn-disabled-spinner');
    }

    Utils.disableButtonWithTimeout = function(button, timeout) {
        Utils.disableButton(button, true);
        setTimeout(function() { Utils.enableButton(button); }, timeout)
    }

    Utils.formatString = function() {
        if (arguments.length < 2) {
            throw '2 or more arguments needed';
        }

        var str = "";
        var params = [];

        for (var argument in arguments) {
            if (argument == 0)
                str = arguments[argument];
            else
                params.push(arguments[argument]);
        }

        for (var param in params)
            str = str.replace(new RegExp('\\{' + param + '\\}', 'gi'), params[param]);

        return str;
    }

    Utils.arrayContains = function (arr, element) {
        for (var i = 0; i < arr.length; i++) {
            if (arr[i] === element) {
                return true
            }
        }
        return false;
    }
    /*
    Utils.requestThrottled = function(url, button, callback) {
        if (window.isRequestThrottledProcessRunning) return;

        window.isRequestThrottledProcessRunning = true;
        Utils.disableButton(button, true);

        Utils.postJSON({
            url: "/service/is_throttling_active/",
            data: { url: url },
            success: function (data) {
                if (data.is_throttled) {
                    toastr.warning("Too many requests, try in " + data.timeout + " seconds");
                    Utils.disableButtonWithTimeout(button, data.timeout * 1000);
                } else {
                    Utils.disableButton(button);
                    callback();
                    Utils.enableButton(button);
                }
                window.isRequestThrottledProcessRunning = false;
            },
            error: function (response) {
                toastr.error(response.responseText);
                window.isRequestThrottledProcessRunning = false;
                Utils.enableButton(button);
            }
        });
    }
    */
}) (Utils);
