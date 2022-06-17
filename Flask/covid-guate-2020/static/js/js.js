function getBotResponse() {
    var rawText = $("#textInput").val();
    if(rawText != ""){
      var userHtml = '<h1> Datos calculados para fecha: ' + rawText + '</h1>';
    }
    $("#textInput").val("");
    $("#chatbox").append(userHtml);    
    document.getElementById('userInput').scrollIntoView({block: 'start', behavior: 'smooth'});

    //Enviar Respuesta al Bot
    $.get("/get", { msg: rawText }).done(function(data) {
      console.log(data)
      var botHtml = '<table class="table table-sm"><thead class="thead-dark" align="center"></tr><tr class="table-primary"><th scope="col" >Infectados</th><th scope="col">Recuperados</th><th scope="col">Fallecidos</th></tr></thead><tbody align="center"><tr style="align-text: center;"><td class="table-primary">'+data["confirmados"]+'</td><td class="table-success">'+data["recuperados"]+'</td><td class="table-danger">'+data["muertos"]+'</td></tr></tbody></table>';
      $("#chatbox").append(botHtml);
      document.getElementById('userInput').scrollIntoView({block: 'start', behavior: 'smooth'});
    });
}

$("#textInput").keypress(function(e) {
    if(e.which == 13) {
        getBotResponse();
    }
});

$("#buttonInput").click(function() {
  getBotResponse();
})

function updateFig(){
  $.get("/fig", { fig: "0" }).done(function(data) {
    if(data == "r"){
      location.reload()
    }
    //console.log(data)
  });
}
