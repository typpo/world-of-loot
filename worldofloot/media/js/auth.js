;function AuthManager() {
  this.Init = function() {
    var me = this;

    // csrf stuff
    function csrfSafeMethod(method) {
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
      crossDomain: false,
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
          xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
      }
    });

    // Login/register button
    $('#login-register-modal a.submit').on('click', function() {
      mixpanel.track('login/register');
      me.Login(
        $('#login-register-username').val(),
        $('#login-register-password').val(),
        $('#login-register-remember-me').prop('checked') ? true : false
      );
      return false;
    });

    // Show modal
    $('a.js-login').on('click', function() {
      mixpanel.track('login/register modal');
      me.ShowLogin();
      return false;
    });

    // Login
    $('#login-register-username, #login-register-password').on('keydown', function(e) {
      if (e.keyCode == 13) {
        $('#login-register-modal a.submit').trigger('click');
      }
    });
  }

  this.ShowLogin = function() {
    $('#login-register-modal').modal();
    $('#login-register-username').focus();
  }

  this.Login = function(username, password, remember) {
    showMessage('Logging in...');
    $.post('/login_or_create/', {
      username: username,
      password: password,
      remember_me: remember
    }, function(data) {
      if (data && data.success)
        window.location.reload()
      else
        alert('Login failed.  Reason: ' + data.reason);
    }, 'json');
  }
}
