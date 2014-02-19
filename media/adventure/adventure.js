$(document).ready(function(){
	var messageNum;
	var newLevel;
	//update so these values can be passed at the loading of the file for loading "save games"
	messageNum = 1;

	$("#message_results").slideUp(); 

    $("#search_button").click(function(e){ 
    	//stops the form from refreshing the page like it normally would.
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
		//I think this is "if you press enter"
		if (code == 13) {
			//sets the textbox value for use in the tryCommand function
			var character_id = $('#character_select').val();
    		var levelNumber = $('#level').val();
    		var gameID = $('#gameID').val();
    		//alert("submit level " + levelNumber);
	  		//alert("submit character " + character_id);
	  		//alert("submit gameid " + gameID);
			ajax_search(this.value, levelNumber, character_id, gameID);
			e.preventDefault();
		}
	});

    function ajax_search(search_val, levelNumber, character_id, gameID){ 
    	//set it to lowercase to make the search simpler
    	search_val = search_val.toLowerCase();
    	//alert("command " + search_val);

    	//go to functions.php with the level #, character, and command to determine the correct story response
	  $.ajax({
	  	 type: "GET",
	  	 url: "functions.php",
	  	 data: {level: levelNumber, characterID: character_id, command: search_val, gameID: gameID},
	  	 dataType: 'JSON',
	  	 success: function(row)
	  	{
	  		//set the storyText equal to the first value in the array from functions.php
	  		//alert(row);
	  		var storyText = row.story;
	  		//set the new level value from functions.php
	  		var newLevel = row.level;

	  		var divString = "<div class='message_results' id='message_results" + messageNum + "'></div>";
			$('#story').append(divString);

		   	//update the message_results field with the $storyText data from functions.php
		    $('#message_results' + messageNum).html(storyText).show("drop", 600); 
		    
		    //empty the command box
		    $('#command').val("");

		    //increment the messageNum
		    messageNum++;

		    //alert("new level ajax " + newLevel);
		    //alert("level " + levelNumber);

		    //call the charachter select function with the new level only if the new level is different from the old
		    if (newLevel != levelNumber){
		    	character_select(newLevel, gameID);
		    	levelNumber = newLevel;
		    }
		    //$('#level').empty();
		    $('#level').val(levelNumber);

		    var saveLink = "<a href='http://www.somesmart.com/max-werner-adv/max-werner.php?levelNumber=" + levelNumber + "'>Your Save Link</a>";
		    $('#save').empty();
		    $('#save').html(saveLink);
		    //alert("now level " + levelNumber);

		    /******************************************************************/
		    /*consider using first = text.slice(0, text.indexOf(" ")); to get just the first word incase they enter more*/
		    /*https://github.com/cameronmcefee/plax*/
		    /*add some code here to store what values people are searching for*/
		    /***********or maybe add said code to the functions file***********/
		    /******************************************************************/

	  	}
	  });
	} 
	function character_select(newLevel, gameID){
		$.post("levelOptions.php", {newLevel: newLevel, gameID: gameID}, function(data){
	   	if (data.length>0){
	   		//clear the existing options
		    $('#character_select').empty();

		    //set the new character select options.
		    $('#character_select').html(data);
	   	}
	   });	
	}
});