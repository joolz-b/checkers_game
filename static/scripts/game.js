
var selectedPiece = null
var selectedCell = null
var refresh = null

function selectCell(pos) {

  if(selectedCell) {
    document.getElementById("cell-" + selectedCell[0] + "-" + selectedCell[1]).style.filter = null
    selectedCell = null
    document.getElementById("game-status-cell").innerHTML = ''
  }

  if(pos) {
    selectedCell = pos
    console.log('selected cell: ' + selectedCell.toString())
    document.getElementById("game-status-cell").innerHTML = 'Selected cell: ' + selectedCell.toString()

    if(selectedPiece.toString().localeCompare(selectedCell.toString()) != 0) {
      document.getElementById("cell-" + selectedCell[0] + "-" + selectedCell[1]).style.filter = "brightness(190%)"
      movePiece()
    }
  }
  
}

function selectPiece(pos) {

  // reset currently selected piece
  if(selectedPiece) {
    document.getElementById("cell-" + selectedPiece[0] + "-" + selectedPiece[1]).style.filter = null
    selectedPiece = null
    document.getElementById("game-status-piece").innerHTML = ''
  }

  if(pos) {

    document.getElementById("game-status-info").innerHTML = ""
    
    selectedPiece = pos
    console.log('selected piece: ' + pos.toString())
    document.getElementById("game-status-piece").innerHTML = 'Selected piece: ' + pos.toString()
    document.getElementById("cell-" + pos[0] + "-" + pos[1]).style.filter = "brightness(190%)"
  }
}

// call backend endpoint here
function movePiece() {

  if(document.getElementById("game-status-current-turn").innerHTML.trim().localeCompare('true') == 0) {
    console.log('moving piece to cell ' + selectedCell.toString())
    document.getElementById("game-status-info").innerHTML = "Moving piece <span id='loader'></span>"
    

    let request = new XMLHttpRequest()
    let game_id = window.location.href.split('/')
    game_id = game_id[game_id.length - 1]

    request.onreadystatechange = function() {
      if (request.readyState == XMLHttpRequest.DONE) {
        if(request.responseText.localeCompare('OK') == 0) {
          location.reload()
        }
        else {
          console.log(request.responseText)
          document.getElementById("game-status-info").innerHTML = "Invalid move. Please select your piece and then select a valid cell."
        }
      }
    }

    request.open("GET", game_id.toString() + '/move?' 
      + 'piece=' + selectedPiece.toString() 
      + '&cell=' + selectedCell.toString()
    )
    request.send()

    // reset selection
    selectCell(null)
    selectPiece(null)
  }
  else {
    console.log('please wait for opponent to complete their turn.')
    document.getElementById("game-status-info").innerHTML = "Please wait for opponent to complete their turn."
  }

  
}

function checkWinner() {
  let request = new XMLHttpRequest()
  let game_id = window.location.href.split('/')
  game_id = game_id[game_id.length - 1]

  request.onreadystatechange = function() {
    if (request.readyState == XMLHttpRequest.DONE) {
  
      if(request.responseText.localeCompare('FALSE') != 0) {
        document.getElementById('banner').innerHTML = request.responseText
        clearTimeout(refresh)
      }
      else {
        console.log('No winner yet for this game...')
      }
    }
  }
  request.open("GET", game_id.toString() + '/check')
  request.send()
}

function setRefreshPage() {
  if(document.getElementById("game-status-current-turn").innerHTML.trim().localeCompare('false') == 0) {
    refresh = setInterval(()=>{
      location.reload()
    }, 10000)
  }
}

window.onload = function() {

  setRefreshPage()
  checkWinner()

}