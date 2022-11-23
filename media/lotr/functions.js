$("#month").change(function(){
	$.find("#event-url").attr("href", "/lotr/event/date/" + $("#month").val() + "/" + $("#day").val() + "/");
});
$("#day").change(function(){
	$.find("#event-url").attr("href", "/lotr/event/date/" + $("#month").val() + "/" + $("#day").val() + "/");
});