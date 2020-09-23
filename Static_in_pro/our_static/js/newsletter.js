 $(document).ready(function(){
//   NEWSLETTER              
        var newsletterForm = $(".ulockd-mailchimp")

        newsletterForm.submit(function(event){
        event.preventDefault();
        console.log("Form is not sending")
        var thisForm = $(this)
        var actionEndpoint = thisForm.attr("action"); // API Endpoint
        var actionEndpoint = thisForm.attr("data-endpoint");
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();

        $.ajax({
          url: actionEndpoint,
          method: httpMethod,
          data: formData,
          success: function(data){
          console.log('proslo')
           
            

          
          },
          
        })
          
    })            
           //NEWSLETTER  
  }) //end ready           