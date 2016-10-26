var debounceTime = 1000;

var $content = $('#content');

function doGithubsJob (input) {
    return input.replace(/\?/g, '%3F').replace('%3Fref=', '?ref=');
}

function list (path) {
    $.get('https://api.github.com/repos/Lyrics/lyrics/contents/' + path)
        .done(function( data ) {
            if (data.length) {
                $content.empty();
                data.forEach(function (item) {
                    var url = doGithubsJob(item.html_url);

                    var $item = $('<div><a href="' + url + '">' + item.name  + '</a></div>');

                    $item.click(function (event) {
                        event.preventDefault();

                        if (item.path.split('/').length < 5)
                            list(item.path);
                        else
                            retrieve(item.download_url);
                    });

                    $content.append($item);
                });
            } else {
                $content.text("Empty directory");
            }
        })
        .fail(function() {
            $content.text("");
        });
};

function retrieve (file) {
    $.get(file)
        .done(function( data ) {
            $content.text(data);
        })
        .fail(function() {
            $content.text("");
        });
}

function retrieveIndirect (file) {
    $.get(file)
        .done(function(data) {
            $.get(data.download_url)
                .done(function(data) {
                    $content.text(data);
                })
                .fail(function() {
                    $content.text("Something went wrong again");
                });
        })
        .fail(function() {
            $content.text("Something went wrong");
        });
}

function find () {
    var query = $(this).val().trim();

    if (query.length < 3) {
        $content.text("");
        return;
    }

    $.get('https://api.github.com/search/code?q=repo:Lyrics/lyrics path:database/ fork:false ' + query)
        .done(function( data ) {
            if (data.total_count) {
                $content.empty();

                data.items.forEach(function (item) {
                    var path = item.path.split('/'); path.shift(); path.shift();
                    var url = doGithubsJob(item.html_url);

                    var $div = $('<div></div>');
                    var $composition = $('<a href="' + url + '">' + item.name  + '</a>');
                    var $artist = $('<a href="' + url + '/../..">' + path[0] + '</a>');
                    var $album = $('<a href="' + url + '/..">' + path[1] + '</a>');
                    $div.append($composition, ' by ', $artist, ' from album ', $album);

                    $content.append($div);

                    $composition.click(function (event) {
                        event.preventDefault();
                        retrieveIndirect(doGithubsJob(item.url));
                    });
                    $artist.click(function (event) {
                        event.preventDefault();
                        list(doGithubsJob(item.path) + '/../..');
                    });
                    $album.click(function (event) {
                        event.preventDefault();
                        list(doGithubsJob(item.path) + '/..');
                    });
                });
            } else {
                $content.text("Nothing found");
            }
        })
        .fail(function() {
            $content.text("Rate limiting is in place, please hold on for a bit");
        });
};

$('#main-content a').click(function (event) {
        event.preventDefault();

        var letter = $(this).text();

        list('database/' + letter);
    });

$('#search').on('input', _.debounce( find, debounceTime ) );
