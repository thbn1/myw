
function pdtabclick(elem){
    var div2=document.getElementById("pddetail");

    var activediv=div2.getElementsByClassName("active")
    activediv[0].setAttribute("class",activediv[0].getAttribute("class").replace(" active",""));
    elem.className += " active";
    const tab=elem.getAttribute("com");
    const es=document.getElementById("tab"+tab);
   
    if(es === null){
        $.ajax({
        
            type: 'GET',
            url: "/pdpage/"+tab,
            data: {},
            success: function (response) {
                document.getElementById('pdtbcont').insertAdjacentHTML("beforeend",response)
                
    
                    
        
        
            },
            error: function (response) {
                console.log(response)
            }
        });
    };
    
    const subtab = document.getElementById("pdtbcont").children;
    for (const sub of subtab) {
        sub.style="display:none;"
    };
    document.getElementById("tab"+tab).style="display:block;"



 };
