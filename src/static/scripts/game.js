
var selectedPiece = null
var selectedCell = null

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

  if(document.getElementById("game-status-current-turn").innerHTML.trim().localeCompare('true') == 0) {
    console.log('moving piece to cell ' + selectedCell.toString())

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
  }

  
}

// call after move function
function checkWinner() {
  let request = new XMLHttpRequest()
  let game_id = window.location.href.split('/')
  game_id = game_id[game_id.length - 1]

  request.onreadystatechange = function() {
    if (request.readyState == XMLHttpRequest.DONE) {
  
      if(request.responseText.localeCompare('FALSE') != 0) {
        document.getElementById('').innerHTML = request.responseText
      }
      else {
        console.log('No winner yet for this game...')
      }
    }
  }
  request.open("GET", game_id.toString() + '/check')
  request.send()
}

window.onload = function() {

  if(document.getElementById("game-status-current-turn").innerHTML.trim().localeCompare('false') == 0) {
    setInterval(()=>{
      location.reload()
    }, 20000)
  }

  checkWinner()

}