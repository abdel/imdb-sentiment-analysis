$(document).ready(function() {
  $('#sentiment-form').submit(function(event) {
    // Stop form from submitting normally
    event.preventDefault();

    // Empty and hide elements
    $('#error').empty().addClass('hidden');
    $('#output-positive').empty().addClass('hidden');
    $('#output-negative').empty().addClass('hidden');

    // Get form values
    const $form = $(this);
    const url = $form.attr( "action");
    const text = $('#text').val().trim();

    // Predict the sentiment
    const predict = $.post(url, { text: text });

    // Handle the response
    predict.done(function(response) {
      const data = JSON.parse(response);

      // Errored
      if (data.error) {
        $('#error').removeClass('hidden');
        $('#output-positive').addClass('hidden');
        $('#output-negative').addClass('hidden');
        return;
      }

      let output
      let outputClass

      // Negative output
      if (data['pred'] === '0') {
        output = `Predicted <strong>negative</strong> sentiment with a probability of ${data['prob']}`;
        outputClass = '#output-negative';

      // Positive output
      } else if (data['pred'] === '1') {
        output = `Predicted <strong>positive</strong> sentiment with a probability of ${data['prob']}`
        outputClass = '#output-positive';
      }

      $(outputClass).empty().removeClass('hidden').append(output);
    });
  });
});