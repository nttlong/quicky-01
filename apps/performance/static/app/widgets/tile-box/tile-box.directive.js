(function () {
    'use strict';

    angular.module('ZebraApp.widgets')
        .directive('tileBox', collapseBox);

    function collapseBox() {
        return {
            restrict: 'E',
            replace: true,
            transclude: true,
            scope: {
                txtTitle: "@title",
                txtheaderInfo: "@info",
                txtDescription: "@description",
                iWidth: "@width",
                txtIcon: "@icon",
                txtNumber: "@number",
                txtColor: "@color",
                imageUrl: "@image",
                iframeUrl: "@iframe",
                color: "@color"
            },
            template: `
                
                <div class="hcs-function-style zb-tile-box-w{{iWidth ? iWidth : 1}}">
                    <div class="hcs-function-title">
                        <div class="hcs-function-title-box">
                            <span class="hcs-function-title-box-1">{{txtTitle}}</span>
                            <span class="hcs-function-title-box-1">{{txtheaderInfo}}</span>
                            <div class="hcs-function-title-box-2">{{txtDescription}}</div>
                        </div>
                    </div>
                    <div class="hcs-function-footer">
                        <div class="hcs-function-title-box">
                            <div class="hcs-function-footer-o hcs-function-footer-t">
                                <div class="hcs-function-footer-th">
                                    <div class="hcs-function-footer-f">
                                        <div class="hcs-function-footer-fi">
                                            <span class="hcs-function-footer-icon {{txtIcon}}">
                                            </span>
                                            <span class="hcs-function-footer-number">{{txtNumber}}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `,
            //templateUrl: "app/components/input/text/text.html",
            link: function ($scope, elem, attr) {
                var header = $(elem).find(".zb-tile-header");
                var headerTitle = $(elem).find(".zb-tile-header-left");
                var headerInfo = $(elem).find(".zb-tile-header-right");
                var contentDescription = $(elem).find(".zb-tile-content-description");

                var content = $(elem).find(".zb-tile-content");
                var contentButton = $(elem).find(".zb-tile-content-bottom");
                var contentNumber = $(elem).find(".zb-tile-content-bottom>.zb-tile-number");
                var contentIcon = $(elem).find(".zb-tile-content-bottom>.zb-tile-icon");

                if ($scope.iframeUrl) {
                    header.remove();
                    content.remove();
                    $(elem).html("<iframe src='" + $scope.iframeUrl + "' width='100%' height='100%' style='border:none'></iframe>");
                } else if ($scope.imageUrl) {
                    header.remove();
                    content.remove();
                    $(elem).html("<img src='" + $scope.imageUrl + "' width='100%' height='100%'/>");
                } else {
                    /*HEADER*/
                    if (!$scope.txtTitle) {
                        header.remove();
                    }

                    if (!$scope.txtheaderInfo) {
                        headerInfo.remove();
                    }

                    if (!$scope.txtDescription) {
                        contentDescription.remove();
                    }
                    /*CONTENT*/
                    if (!$scope.txtIcon && !$scope.txtNumber) {
                        contentButton.remove()
                    } else {
                        if (!$scope.txtIcon) {
                            $scope.txtIcon = "bowtie-icon bowtie-file";
                        }
                    }
                }
                if ($scope.color) {
                    var color = JSON.parse($scope.color);
                    //
                    $(elem).find('span').css({
                        color: color.text
                    })
                    //
                    $(elem).css({
                        background: color.background
                    })
                    //
                    $(elem).find(".hcs-function-title-box-2").css({
                        color: color.text
                    })
                    //
                    $(elem).hover(function (e) {
                        var bsdIn = "0px 0px 0 2px " + color.border;
                        var bsdOut = "none";
                        console.log(color.border)
                        $(this).css('box-shadow', e.type === "mouseenter" ? bsdIn : bsdOut);
                    });
                    //
                    $(elem).find(".hcs-function-footer-icon").css("color", color['color-icon'])
                    //
                    $(elem).find(".hcs-function-footer-number").css("color", color['color-icon'])
                }

                $scope.$applyAsync();
            }
        };
    }
})();