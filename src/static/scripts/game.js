
var selectedPiece = null
var selectedCell = null
var current_turn = null
var player_1 = null
var player_2 = null

function selectCell(pos) {

  if(pos) {
    selectedCell = pos
    console.log('selected cell: ' + pos.toString())
    document.getElementById("game-status-cell").innerHTML = 'Selected cell: ' + pos.toString()

    if(selectedPiece.toString().localeCompare(selectedCell.toString()) != 0) {
      movePiece()
    }
  }
  else {
    selectedCell = null
    document.getElementById("game-status-cell").innerHTML = ''
  }
  
}

function selectPiece(pos) {

  if(pos) {
    
    selectedPiece = pos
    console.log('selected piece: ' + pos.toString())
    document.getElementById("game-status-piece").innerHTML = 'Selected piece: ' + pos.toString()
  }
  else {
    selectedPiece = null
    document.getElementById("game-status-piece").innerHTML = ''
  }
}

// call backend endpoint here
function movePiece() {

  console.log('moving piece to cell ' + selectedCell.toString())

  let request = new XMLHttpRequest()
  let game_id = window.location.href.split('/')
  game_id = game_id[game_id.length - 1]
  console.log(game_id)
  request.open("GET", game_id.toString() + '/move?' + 'piece=' + selectedPiece.toString() + '&cell=' + selectedCell.toString())
  request.send()

  // reset selection
  selectCell(null)
  selectPiece(null)
}

window.onload = function() {
  
  current_turn = document.getElementById("board-current-turn").innerHTML
  player_1 = document.getElementById("board-player-1").innerHTML
  player_2 = document.getElementById("board-player-2").innerHTML
}