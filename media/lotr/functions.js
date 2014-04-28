$("#month").change(function(){
	$("#event-url").attr("href", "/lotr/event/date/" + $("#month").val() + "/" + $("#day").val() + "/");
});
$("#day").change(function(){
	$("#event-url").attr("href", "/lotr/event/date/" + $("#month").val() + "/" + $("#day").val() + "/");
});