#!/usr/bin/perl

use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use JSON qw (encode_json);

use vars qw($LM_HOME);

my $query = new CGI;

my $query = new CGI;
my $mode = $query->param("mode");
my $username = $query->param("username");
my $collection = $query->param("collection");
my $folder = $query->param("folder") || "original_folder";
my $image = $query->param("image") || "img1.png";

##correct original prediction
my $script = system('/media/turing/New Volume/ashutosh/work/work/g_env/bin/python', '/var/www/html/LabelMe/Images/utils/use_xml_to_correct_annotation.py','original_images', $image );

##copy corrected prediction to leftimge8bit for model
$script = system('cp', '/var/www/html/LabelMe/Images/corrected_prediction/'.$image ,'/var/www/html/work/work/dataset/cityscapes/leftImg8bit/val/aachen/aachen_000000_000019_leftImg8bit.png');
$script = system('cp', '/var/www/html/LabelMe/Images/corrected_prediction/'.$image ,'/var/www/html/work/work/dataset/cityscapes/leftImg8bit/train/aachen/aachen_000000_000019_leftImg8bit.png');

##copy corrected prediction gt to gtFine for model
$script = system('cp', '/var/www/html/LabelMe/Images/TrainImgIds/'.$image ,'/var/www/html/work/work/dataset/cityscapes/gtFine/val/aachen/aachen_0000000_000019_gtFine_labelTrainIds.png');#
$script = system('cp', '/var/www/html/LabelMe/Images/TrainImgIds/'.$image ,'/var/www/html/work/work/dataset/cityscapes/gtFine/train/aachen/aachen_0000000_000019_gtFine_labelTrainIds.png');

##read epoch.txt
my $file = "/var/www/html/LabelMe/annotationTools/perl/epoch.txt";
open (CODE, $file) || die "Couldn't open $file: $!";

my $epoch = scalar <CODE>;	#epoch value 

$epoch = $epoch+10;
close(CODE);

open (CODE, '>'.$file) || die "error";
print CODE $epoch;
close(CODE);

##run training
my $script = system('/var/www/html/work/work/g_env/bin/python', '/var/www/html/work/work/erfnet_pytorch/train/main_scribble-Copy1.py', '--datadir', '/var/www/html/work/work/dataset/cityscapes/','--savedir', '/var/www/html/work/work/erfnet_pytorch/save/erfnet_training4', '--num-epochs', $epoch);


##delete xml
my $xml_file = $image =~ s/png/xml/r;
$script = system('rm', '/var/www/html/LabelMe/Annotations/overlayed_images_for_scribbles/'.$xml_file);


my $redirect_url  = "http://localhost/LabelMe/tool.html?collection=LabelMe&mode=f&folder=original_images"."&image=$image";

print "Content-type: application/json\n\n";
my $response->{'redirect_url'} = $redirect_url;
$response->{'curr_dir'} = $script;
my $json_response = JSON::to_json($response);
print $json_response;
