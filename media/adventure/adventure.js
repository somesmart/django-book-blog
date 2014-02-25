$(document).ready(function(){
	var messageNum;
	var newLevel;
	messageNum = 1;

	$("#search_button").click(function(e){ 
		e.preventDefault(); 
		//executes the ajax_search function to get the proper story result.
		ajax_search();
	}); 
	
	//set the character id from the character_select box
	var textBox = $('#command');	
	var code = null;
	textBox.keypress(function(e)
	{
		code = (e.keyCode ? e.keyCode : e.which);
		if (code == 13) {
			//sets the textbox value for use in the tryCommand function
			var character_id = $('#character_select').val();
			var levelNumber = $('#level').val();
			var gameID = $('#gameID').val();
			ajax_search(this.value, levelNumber, character_id, gameID);
			e.preventDefault();
		}
	});

	function ajax_search(search_val, levelNumber, character_id, gameID){ 
	//set it to lowercase to make the search simpler
	search_val = search_val.toLowerCase();

	$.ajax({
		type: "GET",
		url: "/adventure/story/" + search_val + "/" + gameID + "/" + character_id + "/" + levelNumber + "/",
		success: function(data)
		{
			$(data).each(function(k,v){
				//alert(v.text);
				var storyText = v.text;
				var newLevel = v.next_level;
				var story_id = v.id;
				var divString = "<div class='message_results' id='message_results" + messageNum + "'></div>";
				$('#game-div').append(divString);

				//update the message_results field with the $storyText data 
				$('#message_results' + messageNum).html(storyText).show("drop", 600); 
				
				//empty the command box
				$('#command').val("");

				//increment the messageNum
				messageNum++;

				//call the charachter select function with the new level only if the new level is different from the old
				if (newLevel != levelNumber){
					character_select(newLevel, gameID);
				}
				//$('#level').empty();
				$('#level').val(newLevel);

				var saveLink = "<a href='/adventure/game/" + gameID + "/" + character_id + "/" + levelNumber + "/?story_id=" + story_id + "'>Your Save Link</a>";
				$('#save').empty();
				$('#save').html(saveLink);
			});
		}
	});
	}
	function character_select(newLevel, gameID){
		$.get("/adventure/level/option/" + gameID + "/" + newLevel + "/", function(data){
		if (data.length>0){
			//clear the existing options
			$('#character_select').empty();

			//set the new character select options.
			$('#character_select').html(data);
		}
	});
	}
});