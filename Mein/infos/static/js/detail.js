
$(document).ready(function(){
    var tem = '<div class="card flex-md-row h-md-250">';
        tem += '<div class="card-body flex-column align-items-start">';
        tem += '<span class="text-secondary" style="font-size:large;">등급안내</span></br>'
        tem += '<span class="text-info">1등급: ';
        for(var i=0; i<5; i++) tem+='<img class="grade_img" src="../../static/img/award.png">';
        tem += '<span class="text-info ml-2">2등급: ';
        for(var i=0; i<4; i++) tem+='<img class="grade_img" src="../../static/img/award.png">';
        tem += '<span class="text-info ml-2">3등급: ';
        for(var i=0; i<3; i++) tem+='<img class="grade_img" src="../../static/img/award.png">';
        tem += '</br><span class="text-info">4등급: ';
        for(var i=0; i<2; i++) tem+='<img class="grade_img" src="../../static/img/award.png">';
        tem += '<span class="text-info ml-5">5등급: ';
        tem +='<img class="grade_img" src="../../static/img/award.png">';
        tem += '<span class="text-info ml-5">평가제외: ';
        tem +='<img class="grade_img" src="../../static/img/exception.png">';

        tem += '</div></div>';

    $("#grade_header").popover({content: "template", template:tem, trigger:"hover", placement: "top"}).hover(function(){
                                    $(this).css("cursor", "pointer")}, function(){$(this).css("cursor", "default")});
});
