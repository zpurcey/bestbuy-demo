$(document).ready(function() {

  // remote
  // ------

  var bestProducts = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.nonword('value'),
    queryTokenizer: Bloodhound.tokenizers.nonword,
    prefetch: 'http://localhost:8080/api/v1/search?q=google',
    remote: {
      url: 'http://localhost:8080/api/v1/search?q=%QUERY',
      wildcard: '%QUERY'
    }
  });

  $('#remote .typeahead').typeahead({
    hint: false,
    highlight: true,
    minLength: 3
  }, {
    name: 'best-products',
    source: bestProducts,
    limit: 13
  });

});
