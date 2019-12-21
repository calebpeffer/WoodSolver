$(function(){
    $('button').click(function(){
       

        this.counter++;
        var pieces = $('#piecesId').val();
        var stock_options = $('#stockOptionsId').val();
        // if(typeof this.prevPieces == 'undefined' ) {
        //     this.prevPieces = pieces
        // } else if (this.prevPieces == pieces){
        //    return;
        // }

        

        // if(typeof this.prevOptions == 'undefined') {
        //     this.prevOptions = stock_options;
        // } else if( this.prevOptions == stock_options){
        //     return;
        // }
        
        $.ajax({
            url: '/api/solve',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
                var responseJson = JSON.parse(response)
                console.log(responseJson);
                parseResponse(responseJson);

                // console.log(responseJson.status);

            },
            error: function(error){
                console.log(error);
            }

        });
    });
});

function parseResponse (responseJson) {
    // grabs relevant data from response
    var numOfBeams = responseJson["num_beams"];
    var beamsData = responseJson["solver"].split(",");
    console.log(numOfBeams);
    console.log(beamsData);
    
   
    var resultsContainer = $("#results_container");
    resultsContainer.html(""); //clear element before populating it
    var numOfBeamsContainer = document.createElement("h3");
    numOfBeamsContainer.innerText = "Total Number of Beams: " + numOfBeams;
    resultsContainer.append(numOfBeamsContainer);
    for(let i = 0; i < beamsData.length; i++){
        var beamLayoutContainer = document.createElement("div");
        beamLayoutContainer.innerHTML = beamsData[i];
        resultsContainer.append(beamLayoutContainer);
    }
    

}