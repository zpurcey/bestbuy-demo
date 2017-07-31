$(document).ready(function() {

  // remote
  // ------

  var bestProducts = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.nonword('value'),
    queryTokenizer: Bloodhound.tokenizers.nonword,
    prefetch: '/es/api/v1/search?q=google',
    remote: {
      url: '/es/api/v1/search?q=%QUERY',
      wildcard: '%QUERY'
    }
  });

  $('#remote .typeahead').typeahead({
    hint: false,
    highlight: true,
    minLength: 1
  }, {
    name: 'best-products',
    source: bestProducts,
    limit: 13
  });

});
