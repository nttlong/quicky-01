(function () {
    'use strict';

    angular.module('ZebraApp.widgets')
        .directive('collapseBoxHome', collapseBoxHome);

    function collapseBoxHome() {
        return {
            restrict: 'E',
            replace: true,
            transclude: true,
            // scope: {
            //     txtTitle: "@title",
            //     txtDescription: "@description"
            // },
            template: '' +
                '<div class="zb-collapse-box">' +
                '   <div class="zb-header hcs-zb-header-custom">' +
                '       <header class="zb-header-box">' +
                '          <div class="zb-header-content hcs-zb-header-content-custom">' +
                '              <span class="zb-header-icon hcs-zb-header-icon-custom">' +
                '                  <i class="sap-icon sap-navigation-down-arrow zb-icon-up hcs-zb-icon-up-custom"></i>' +
                '              </span>' +
                '              <div class="zb-header-content-box">' +
                '                   <div class="zb-header-content-box-txt">' +
                '                       <div class="zb-header-content-box-title">' +
                '                           <span class="zb-header-title"></span>' +
                '                           <span class="zb-header-title-o"></span>' +
                '                       </div>' +
                '                       <div class="zb-header-content-box-des">' +
                '                           <span class="zb-header-description hcs-zb-header-description-custom"></span>' +
                '                       </div>' +
                '                   </div>' +
                '              </div>' +
                '          </div>' +
                '       </header>' +
                '       <div class="zb-header-right hcs-zb-header-right-custom"></div>' +
                '   </div>' +
                '   <div class="zb-content hcs-zb-content-custom"></div>' +
                '</div>',
            //templateUrl: "app/components/input/text/text.html",
            link: function ($scope, elem, attr, ctrls, $transclude) {
                var $config = {
                    txtTitle: attr["title"],
                    txtDescription: attr["description"],
                    txtNumber: attr["number"],
                    icon: attr["icon"],
                    underline: attr["underline"]
                };

                var header  = $(elem).find('.zb-header.hcs-zb-header-custom');
                var headerIcon = $(elem).find(".zb-header-icon");
                var headerTitle = $(elem).find(".zb-header-title");
                var _headerTitle = $(elem).find(".zb-header-title-o");
                var collapseIcon = $config.icon ? '<i style="font-size: 20px; padding: 0px 10px 0px 0px;" class="' + $config.icon + '"></i>' : '';
                var headerNumber = $(elem).find(".zb-header-number");
                var headerDescription = $(elem).find(".zb-header-description");
                var content = $(elem).find(".zb-content");

                $transclude($scope, function (nodes) {
                    $.each(nodes, function (i, v) {
                        if (v.tagName && v.tagName.toLowerCase() == "toolbar") {
                            $(elem).find(".zb-header-right").append(v)
                        } else {
                            $(elem).find(".zb-content").append(v);
                        }
                    });
                })

                if($config.underline === 'false'){
                    header.addClass('no-underline');
                }
                var txtT = $config.txtTitle.split('\n')
                headerTitle.html(collapseIcon + txtT && txtT.length > 0 ? txtT[0] : $config.txtTitle);
                _headerTitle.html(txtT && txtT.length > 0 ? txtT[1] : '');
                headerNumber.html($config.txtNumber);
                headerDescription.html($config.txtDescription);
                if (!$config.txtDescription) {
                    headerDescription.remove();
                }

                var _collapse = function () {
                    if (content.is(":hidden")) {
                        headerIcon.find("i").addClass("zb-icon-up");
                        headerIcon.find("i").removeClass("zb-icon-down");
                    } else {
                        headerIcon.find("i").removeClass("zb-icon-up");
                        headerIcon.find("i").addClass("zb-icon-down");
                    }
                    var toggle = content.slideToggle(300);
                }
                headerIcon.bind("click", _collapse);
                headerTitle.bind("click", _collapse);
                resizeCSS();
                function resizeCSS() {
                    var wdWidth = $(window).width();
                    var sSizeL = 0;
                    var sSizeR = 0;
                    var pWLeft = 0;
                    var pWRight = 0;

                    if (wdWidth > 1137) {
                        sSizeL = 1138;
                        sSizeR = 1138;
                    } else if (wdWidth > 950) {
                        sSizeL = 951;
                        sSizeR = 951;
                    } else if (wdWidth > 764) {
                        sSizeL = 764;
                        sSizeR = 764;
                    } else if (wdWidth > 600) {
                        sSizeL = 577;
                        sSizeR = 577;
                    } else if (wdWidth > 480) {
                        sSizeL = 481;
                        sSizeR = 481;
                    } else {
                        sSizeL = 326;
                        sSizeR = 326;
                    }
                    pWLeft = (wdWidth - sSizeL) / 2;
                    pWRight = (wdWidth - sSizeR) / 2;
                    $(elem).find("header").css({
                        "padding-left": (pWLeft - 48) + "px",
                        "padding-right": (pWRight - 48) + "px"
                    });
                    $(elem).find(".container-fluid").css({
                        "padding-left": (pWLeft) + "px",
                        "padding-right": (pWRight) + "px"
                    });
                };
            }
        };
    }
})();