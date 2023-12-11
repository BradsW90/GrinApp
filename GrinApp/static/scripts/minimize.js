document.addEventListener("DOMContentLoaded", function () {
    //comment section references
    const miniComment = document.getElementById('miniComment');
    const commentList = document.getElementById('commentList');
    //service list references
    const miniService = document.getElementById('miniService');
    const serviceList = document.getElementById('serviceList');
    //new service list references
    const miniNewService = document.getElementById('miniNewService');
    const newServiceList = document.getElementById('newServiceList')

    //Gives minimize function to each function call
    minimize(miniComment, commentList);
    minimize(miniService, serviceList);
    minimize(miniNewService, newServiceList);

    //Contains core minimize function code
    function minimize(button, dataList) {
        button.addEventListener('click', function() {
            var data = dataList.children;
            for (i=0; i<data.length; i++) {
                let isHidden = data[i].hasAttribute('hidden');
                if (isHidden) {
                    data[i].removeAttribute('hidden');
                } else {
                    data[i].setAttribute('hidden', true);
                }
            }
        });
    };
});