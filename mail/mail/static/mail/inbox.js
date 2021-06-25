document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  const send = document.querySelector('.btn.btn-primary')
  send.onclick = () => {
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    fetch('emails/', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
      })
    })
    .then(response => response.json())
    .then(result => {
      // Print result
      console.log(result);
      alert(result);
      // If success return to sent inbox with load function
      // else return an alert stating error
    });
    return load_mailbox('sent');
    
  }
}



function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => { 
    if (emails.length != 0) {
    
      emails.forEach(email => {
      const div = document.createElement('div');
      div.innerHTML = email.subject;

      document.addEventListener('click', function() {
        // Archive button
        console.log('button clicked');
      });

      document.querySelector('#emails-view').append(div);
    });
    }
    else {
      
      const div = document.createElement('div');
      div.innerHTML = `Your ${mailbox} mailbox is empty`;
      document.querySelector('#emails-view').append(div);
    }
    
    
  });
}


function load_mail(mail_id) {

  //function that opens an email


}