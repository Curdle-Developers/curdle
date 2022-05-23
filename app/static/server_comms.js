/**
 * Retrieves the list of possible cheeses from the server.
 * @returns list of possible cheeses.
 */
function getCheeseList() {
  let response
  $.ajax({
    type: "POST",
    async: false,
    url: '/get-cheeses',
    dataType: "json",
    success: function (data, status, xhr) { response=data;}
  });
  let cheeseList = Object.values(response);
  return cheeseList;
}

/**
 * Function returns an array of boolean data for checking if the guesses attributes
 * align with the answers attributes.
 * @param entry the cheese value entered into guess box.
 * @returns array of guess results from the server.
 */
function sendCheese(entry) {
  let response
  $.ajax({
    type: "POST",
    async: false,
    url: '/check-guess',
    contentType: "application/json",
    dataType: "json",
    data: JSON.stringify({
      cheese_name: entry,
    }),
    success: function (data, status, xhr) { response=data;}
  });
  
  // Arranges the JSON as some browsers alphabetically order it :/
  let result_arranged = [];
  result_arranged.push(response.name)
  result_arranged.push(response.country)
  result_arranged.push(response.mould)
  result_arranged.push(response.animal)
  result_arranged.push(response.type)
  result_arranged.push(response.continent)
  return result_arranged;
}

/**
 * Function retrieves the day's puzzle id. Used in tracking stats.
 */
function getPuzzleID() {
  let response;
  $.ajax({
    type: "POST",
    async: false,
    url: '/puzzle-id',
    dataType: "json",
    success: function (data, status, xhr) { response=data;}
  });
  let puzzleData = Object.values(response);
  puzzleNum = puzzleData[1];
}

/**
 * Function retrieves the answer to the puzzle and links to resources used. 
 * Revealed to users if they fail to guess.
 * @return an array containing the answer, its attributes, and references.
 */
function getAnswer() {
  let response;
  $.ajax({
    type: "POST",
    async: false,
    url: '/get-answer',
    dataType: "json",
    success: function (data, status, xhr) { response=data;}
  });
  let result_arranged = [];
  // Arranges the JSON as some browsers alphabetically order it :/
  result_arranged.push(response.name)
  result_arranged.push(response.continent)
  result_arranged.push(response.country)
  result_arranged.push(response.mouldy)
  result_arranged.push(response.animal)
  result_arranged.push(response.type)
  result_arranged.push(response.image_attribution)
  result_arranged.push(response.info_link)

  //Generates text in the answer info pop up.
  $("#correct-cheese p").html(result_arranged[0]);
  $("#answer-name").html(result_arranged[0]);
  $("#answer-region").html("The region of origin is: " + result_arranged[1]);
  $("#answer-country").html("The country of origin is: " + result_arranged[2]);
  if (result_arranged[3] == true) {
    $("#answer-mould").html("The cheese contains veins.");
  } else {
    $("#answer-mould").html("The cheese does not contain veins.");
  }
  $("#answer-animal").html("The animal of origin is: " + result_arranged[4]);
  $("#answer-type").html("The type of cheese is: " + result_arranged[5]);
  //Attaches href to references that appear at bottom of page.
  $("#info-ref").attr("href", result_arranged[7]);
  $("#image-ref").attr("href", result_arranged[6]);
  $("#references").css("display", "flex").hide().fadeIn("slow");

  return result_arranged;
}

/**
 * Functions for forcing a new puzzle.
 */
 function resetServerPuzzleHistory() {
  let response;
  $.ajax({
    type: "POST",
    async: false,
    url: '/reset-puzzle-history',
    dataType: "json",
    success: function (data, status, xhr) { response=data; console.log(data);}
  });
}

function incrementPuzzleID() {
  let response;
  $.ajax({
    type: "POST",
    async: false,
    url: '/increment-puzzle-id',
    dataType: "json",
    success: function (data, status, xhr) { response=data; console.log(data);}
  });
}