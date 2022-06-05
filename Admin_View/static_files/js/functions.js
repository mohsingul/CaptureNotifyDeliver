
$(document).ready( function() {

    $("#about-btn").click( function(event) {
        alert("You clicked the button using JQuery!");

    });
});

$(#mytable).dataTables();

$(document).ready(function(){

  $(".dateinput").datepicker({changeYear: true,changeMonth: true});


});

//function home()
//{
//    document.getElementById('div_home').style.visibility="visible"
//}



function allpackages() {

    document.getElementById("div_home").style.visibility="hidden"
    document.getElementById("div_output").style.visibility="hidden"
    document.getElementById("div_alldata").style.visibility="visible"



    }

function btn_name()
{

    document.getElementById('div_output').style.visibility="visible";

}




//$(document).on("click", ".browse", function() {
//  var file = $(this).parents().find(".file");
//  file.trigger("click");
//});
//$('input[type="file"]').change(function(e) {
//  var fileName = e.target.files[0].name;
//  $("#file").val(fileName);
//
//  var reader = new FileReader();
//  reader.onload = function(e) {
//    // get loaded data and render thumbnail.
//    document.getElementById("preview").src = e.target.result;
//  };
//  // read the image file as a data URL.
//  reader.readAsDataURL(this.files[0]);
//});


function ajax_get_update()
    {
       $.get(url, function(results){
          //get the parts of the result you want to update. Just select the needed parts of the response
          var table = $("table", results);
          var span = $("span.step-links", results);

          //update the ajax_table_result with the return value
          $('#ajax_table_result').html(table);
          $('.step-links').html(span);
        }, "html");
    }

//bind the corresponding links in your document to the ajax get function
$( document ).ready( function() {
    $( '.step-links #prev' ).click( function(e) {
        e.preventDefault();
        url = ($( '.step-links #prev' )[0].href);
        ajax_get_update();
    });
    $( '.step-links #next' ).click( function(e) {
        e.preventDefault();
        url = ($( '.step-links #next' )[0].href);
        ajax_get_update();

    });
});

//since the links are reloaded we have to bind the links again
//to the actions
$( document ).ajaxStop( function() {
    $( '.step-links #prev' ).click( function(e) {
        e.preventDefault();
        url = ($( '.step-links #prev' )[0].href);
        ajax_get_update();
    });
    $( '.step-links #next' ).click( function(e) {
        e.preventDefault();
        url = ($( '.step-links #next' )[0].href);
        ajax_get_update();
    });
});







$('#fileup').change(function(){

    var res=$('#fileup').val();
    var arr = res.split("\\");
    var filename=arr.slice(-1)[0];
    filextension=filename.split(".");
    filext="."+filextension.slice(-1)[0];
    valid=[".jpg",".png",".jpeg",".bmp"];
//if file is not valid we show the error icon, the red alert, and hide the submit button
    if (valid.indexOf(filext.toLowerCase())==-1){
        $( ".imgupload" ).hide("slow");
        $( ".imgupload.ok" ).hide("slow");
        $( ".imgupload.stop" ).show("slow");

        $('#namefile').css({"color":"red","font-weight":700});
        $('#namefile').html("File "+filename+" is not  pic!");

        $( "#submitbtn" ).hide();
        $( "#fakebtn" ).show();
    }else{
        //if file is valid we show the green alert and show the valid submit
        $( ".imgupload" ).hide("slow");
        $( ".imgupload.stop" ).hide("slow");
        $( ".imgupload.ok" ).show("slow");

        $('#namefile').css({"color":"green","font-weight":700});
        $('#namefile').html(filename);

        $( "#submitbtn" ).show();
        $( "#fakebtn" ).hide();
    }
});


$(document).on("click", ".browse", function() {
  var file = $(this)
    .parent()
    .parent()
    .parent()
    .find(".file");
  file.trigger("click");
});
$(document).on("change", ".file", function() {
  $(this)
    .parent()
    .find(".form-control")
    .val(
      $(this)
        .val()
        .replace(/C:\\fakepath\\/i, "")
    );
});
$document.ready
const inpFile= document.getElementById("inpfile");
const previewContainer=document.getElementById("imagepreview");
const previewImage= previewContainer.querySelector(".image-preview__image");
const preventDefaultText= previewContainer.querySelector(".image-preview__default-text");
inpFile.addEventListener("change",function())
{
    const file= this.files[0];
    console.log(file)


}


