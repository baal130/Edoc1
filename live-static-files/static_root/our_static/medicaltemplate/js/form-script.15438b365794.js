/*!
 * Version v0.01.0 for
 * Copyright 2017 Unlock Design
 * Licensed under http://unlockdesizn.com
 * https://themeforest.net/user/unlockdesign
 *
 */

+function ($) {
  'use strict';

  // VALIDATOR CLASS DEFINITION
  // ==========================
 
  // CONTACT FORM 1 SCRIPT
  // ===========================
  $(function () {
      $('#contact_form').validator();
      $('#contact_form').on('submit', function (e) {
          if (!e.isDefaultPrevented()) {
            var url = "includes/contact.php";
            $.ajax({
                type: "POST",
                url: url,
                data: $(this).serialize(),
                success: function (data)
                {
                    var messageAlert = 'alert-' + data.type;
                    var messageText = data.message;

                    var alertBox = '<div class="alert ' + messageAlert + ' alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + messageText + '</div>';
                    if (messageAlert && messageText) {
                        $('#contact_form').find('.messages').html(alertBox).fadeIn('slow');
                        $('#contact_form')[0].reset();
                        setTimeout(function(){ $('.messages').fadeOut('slow') }, 6000);
                    }
                }
            });
            return false;
          }
      })
  });
 
  // CONTACT FORM 2 SCRIPT
  // ===========================
  $(function () {
      $('#contact_form2').validator();
      $('#contact_form2').on('submit', function (e) {
          if (!e.isDefaultPrevented()) {
            var url = "includes/contact2.php";
            $.ajax({
                type: "POST",
                url: url,
                data: $(this).serialize(),
                success: function (data)
                {
                  var messageAlert = 'alert-' + data.type;
                  var messageText = data.message;

                  var alertBox = '<div class="alert ' + messageAlert + ' alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + messageText + '</div>';
                  if (messageAlert && messageText) {
                      $('#contact_form2').find('.messages').html(alertBox).fadeIn('slow');
                      $('#contact_form2')[0].reset();
                      setTimeout(function(){ $('.messages').fadeOut('slow') }, 6000);
                  }
                }
            });
            return false;
          }
      })
  });

  // APPOINTMENT FORM 1 SCRIPT
  // ===========================
  $(function () {
      $('#appointment_form').validator();
      $('#appointment_form').on('submit', function (e) {
        if (!e.isDefaultPrevented()) {
          var url = "includes/appointment.php";
          $.ajax({
              type: "POST",
              url: url,
              data: $(this).serialize(),
              success: function (data)
              {
                var messageAlert = 'alert-' + data.type;
                var messageText = data.message;

                var alertBox = '<div class="alert ' + messageAlert + ' alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + messageText + '</div>';
                if (messageAlert && messageText) {
                    $('#appointment_form').find('.messages').html(alertBox).fadeIn('slow');
                    $('#appointment_form')[0].reset();
                    setTimeout(function(){ $('.messages').fadeOut('slow') }, 6000);
                }
              }
          });
          return false;
        }
      })
  });

  // BOOKING FORM 1 SCRIPT
  // =====================
  $(function () {
      $('#booking_form').validator();
      $('#booking_form').on('submit', function (e) {
          if (!e.isDefaultPrevented()) {
            var url = "includes/booking.php";
            $.ajax({
                type: "POST",
                url: url,
                data: $(this).serialize(),
                success: function (data)
                {
                console.log(data);
                  var messageAlert = 'alert-' + data.type;
                  var messageText = data.message;

                  var alertBox = '<div class="alert ' + messageAlert + ' alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + messageText + '</div>';
                  if (messageAlert && messageText) {
                      $('#booking_form').find('.messages').html(alertBox).fadeIn('slow');
                      $('#booking_form')[0].reset();
                      setTimeout(function(){ $('.messages').fadeOut('slow') }, 6000);
                  }
                }
            });
            return false;
          }
      })
  });

  // BOOKING FORM 2 SCRIPT
  // =====================
  $(function () {
      $('#booking_form').validator();
      $('#booking_form').on('submit', function (e) {
          if (!e.isDefaultPrevented()) {
            var url = "includes/booking2.php";
            $.ajax({
                type: "POST",
                url: url,
                data: $(this).serialize(),
                success: function (data)
                {
                  console.log(data);
                  var messageAlert = 'alert-' + data.type;
                  var messageText = data.message;

                  var alertBox = '<div class="alert ' + messageAlert + ' alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + messageText + '</div>';
                  if (messageAlert && messageText) {
                      $('#booking_form').find('.messages').html(alertBox).fadeIn('slow');
                      $('#booking_form')[0].reset();
                      setTimeout(function(){ $('.messages').fadeOut('slow') }, 6000);
                  }
                }
            });
            return false;
          }
      })
  });

  // BOOKING FORM 3 SCRIPT
  // =====================
  $(function () {
      $('#booking_form').validator();
      $('#booking_form').on('submit', function (e) {
          if (!e.isDefaultPrevented()) {
            var url = "includes/booking3.php";
            $.ajax({
                type: "POST",
                url: url,
                data: $(this).serialize(),
                success: function (data)
                {
                  console.log(data);
                  var messageAlert = 'alert-' + data.type;
                  var messageText = data.message;

                  var alertBox = '<div class="alert ' + messageAlert + ' alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + messageText + '</div>';
                  if (messageAlert && messageText) {
                      $('#booking_form').find('.messages').html(alertBox).fadeIn('slow');
                      $('#booking_form')[0].reset();
                      setTimeout(function(){ $('.messages').fadeOut('slow') }, 6000);
                  }
                }
            });
            return false;
          }
      })
  });

  // JOB APPLY FORM 1 SCRIPT
  // =====================
    $(function () {
        $('#jobapply_form').validator();
        $('#jobapply_form').on('submit', function (e) {
            var formData = new FormData($('form#jobapply_form')[0]);
            if (!e.isDefaultPrevented()) {
                var url = "includes/job.php";
                $.ajax({
                    type: "POST",
                    url: url,
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function (data)
                    {
                      var messageAlert = 'alert-' + data.type;
                      var messageText = data.message;

                      var alertBox = '<div class="alert ' + messageAlert + ' alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + messageText + '</div>';
                      if (messageAlert && messageText) {
                          $('#jobapply_form').find('.messages').html(alertBox).fadeIn('slow');
                          $('#jobapply_form')[0].reset();
                          setTimeout(function(){ $('.messages').fadeOut('slow') }, 6000);
                      }
                    }
                });
                return false;
            }
        })
    });

  // JOB APPLY FORM 2 SCRIPT
  // =====================
    $(function () {
        $('#jobapply_form').validator();
        $('#jobapply_form').on('submit', function (e) {
            var formData = new FormData($('form#jobapply_form')[0]);
            if (!e.isDefaultPrevented()) {
              var url = "includes/job2.php";
              $.ajax({
                  type: "POST",
                  url: url,
                  data: formData,
                  processData: false,
                  contentType: false,
                  success: function (data)
                  {
                    console.log(data);
                    var messageAlert = 'alert-' + data.type;
                    var messageText = data.message;

                    var alertBox = '<div class="alert ' + messageAlert + ' alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + messageText + '</div>';
                    if (messageAlert && messageText) {
                        $('#jobapply_form').find('.messages').html(alertBox).fadeIn('slow');
                        $('#jobapply_form')[0].reset();
                        setTimeout(function(){ $('.messages').fadeOut('slow') }, 6000);
                    }
                  }
              });
              return false;
            }
        })
    });

  // VALIDATOR DATA-API
  // ==================

}(jQuery);
