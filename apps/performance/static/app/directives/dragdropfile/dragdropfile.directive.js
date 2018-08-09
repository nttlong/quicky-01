(function() {
    'use strict';

    angular
        .module('hcs-template')
        .directive('templateDragDrop', dragdrop);

    dragdrop.$inject = ['templateService'];
    
    function dragdrop(templateService) {
        // Usage:
        //     <input-combobox></input-combobox>
        // Creates:
        // 
        var directive = {
            link: link,
            restrict: 'EA',
            scope: {
                limitCondition: "=",
                currentItem: "="
            },
            templateUrl: templateService.getTemplatePath('dragdropfile')
        };
        return directive;

        function link(scope, element, attrs) {
            DropAndDrag(scope, element, attrs);
        }

        function DropAndDrag(scope, element, attrs) {
            var dropzone = new Dropzone('#demo-upload', {
                maxFiles: 1,
                init: function () {
                    var me = this;
                    this.on("maxfilesexceeded", function (file) {
                        this.removeAllFiles();
                        this.addFile(file);
                        readFile(file);
                    });
                    if (scope.currentItem) {
                        var val = scope.currentItem;
                        var mockFile = {
                            name: val.file_name,
                            size: val.file_size,
                            type: val.file_type,
                            thumbnail: val,
                            accepted: true
                        };
                        me.files.push(mockFile);    // add to files array
                        me.emit("addedfile", mockFile);
                        me.emit("thumbnail", mockFile, val.file_thumbnail);
                        me.emit("complete", mockFile);
                    }
                },
                previewTemplate: document.querySelector('#preview-template').innerHTML,
                parallelUploads: 2,
                thumbnailHeight: 32,
                thumbnailWidth: 32,
                maxFilesize: 3,
                filesizeBase: 1000,
                thumbnail: function (file, dataUrl) {
                    if (file.previewElement) {
                        file.previewElement.classList.remove("dz-file-preview");
                        var images = file.previewElement.querySelectorAll("[data-dz-thumbnail]");
                        for (var i = 0; i < images.length; i++) {
                            var thumbnailElement = images[i];
                            thumbnailElement.alt = file.name;
                            thumbnailElement.src = dataUrl;
                        }
                        setTimeout(function () { file.previewElement.classList.add("dz-image-preview"); }, 1);
                    }
                },
            });


            // Now fake the file upload, since GitHub does not handle file uploads
            // and returns a 404

            var minSteps = 6,
                maxSteps = 60,
                timeBetweenSteps = 100,
                bytesPerStep = 100000;

            dropzone.uploadFiles = function (files) {
                var self = this;
                for (var i = 0; i < files.length; i++) {
                    var file = files[i];
                    readFile(file);
                    var totalSteps = Math.round(Math.min(maxSteps, Math.max(minSteps, file.size / bytesPerStep)));
                    for (var step = 0; step < totalSteps; step++) {
                        var duration = timeBetweenSteps * (step + 1);
                        setTimeout(function (file, totalSteps, step) {
                            return function () {
                                file.upload = {
                                    progress: 100 * (step + 1) / totalSteps,
                                    total: file.size,
                                    bytesSent: (step + 1) * file.size / totalSteps
                                };
                                self.emit('uploadprogress', file, file.upload.progress, file.upload.bytesSent);
                                if (file.upload.progress == 100) {
                                    file.status = Dropzone.SUCCESS;
                                    self.emit("success", file, 'success', null);
                                    self.emit("complete", file);
                                    self.processQueue();
                                    //document.getElementsByClassName("dz-success-mark").style.opacity = "1";
                                }
                            };
                        }(file, totalSteps, step), duration);
                    }
                }
            }

            function getExtension(ext) {
                var url = '';
                switch (ext.toLowerCase()) {
                    case 'docx':
                    case 'doc':
                        url = 'https://image.flaticon.com/icons/svg/28/28863.svg'
                        break;
                    case 'xls':
                    case 'xlsx':
                        url = 'https://image.flaticon.com/icons/svg/29/29070.svg'
                        break;
                    case 'img':
                    case 'png':
                    case 'jpg':
                        url = 'https://image.flaticon.com/icons/svg/29/29264.svg'
                        break;
                    default:
                        url = 'https://image.flaticon.com/icons/svg/28/28842.svg'
                }
                return url;
            }

            function readFile(file) {
                var reader = new FileReader();
                reader.onload = function () {
                    var obj = {};
                    var dataURL = reader.result;
                    obj.file_name = file.name;
                    obj.file_type = file.type;
                    obj.file_size = file.size;
                    obj.file_data = dataURL;
                    obj.file_extends = file.name.split('.')[1];
                    if (file.previewElement) {
                        file.previewElement.classList.remove("dz-file-preview");
                        var images = file.previewElement.querySelectorAll("[data-dz-thumbnail]");
                        for (var i = 0; i < images.length; i++) {
                            var thumbnailElement = images[i];
                            thumbnailElement.alt = file.name;
                            thumbnailElement.src = getExtension(file.name.split('.')[1]);
                            obj.file_thumbnail = getExtension(file.name.split('.')[1]);
                        }
                        setTimeout(function () { file.previewElement.classList.add("dz-image-preview"); }, 1);
                    }
                    scope.currentItem = obj;
                    scope.$applyAsync();
                };
                reader.readAsDataURL(file);
            }

            function confirm(callback) {
                dropzone.confirm = function (question, accepted, rejected) {
                    if (accepted) {
                        callback();
                    }
                };
            }

            
        }

    }

})();