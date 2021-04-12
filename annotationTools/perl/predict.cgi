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



##replace weights with pretrained weights

##copy original image to leftimge8bit for model
my $script = system('cp', '/var/www/html/LabelMe/Images/original_images/'.$image ,'/var/www/html/work/work/dataset/cityscapes/leftImg8bit/val/aachen/aachen_000000_000019_leftImg8bit.png');

##copy original image to labeltrainIds for model
$script = system('cp', '/var/www/html/LabelMe/Images/original_images/'.$image ,'/var/www/html/work/work/dataset/cityscapes/gtFine/val/aachen/aachen_0000000_000019_gtFine_labelTrainIds.png');


##run prediction
$script = system('/var/www/html/work/work/g_env/bin/python', '/var/www/html/work/work/erfnet_pytorch/eval/eval_cityscapes_color.py', '--datadir', '/var/www/html/work/work/dataset/cityscapes/','--loadDir', '/var/www/html/work/work/erfnet_pytorch/save/erfnet_training4/', '--subset', 'val');

##copy prediction of model to original_predictions folder
$script = system('cp', '/var/www/html/work/work/erfnet_pytorch/eval/save_color/val/aachen/aachen_000000_000019_leftImg8bit.png' ,'/var/www/html/LabelMe/Images/original_predictions/'.$image);

##overlay images for scribbles
$script = system('/media/turing/New Volume/ashutosh/work/work/g_env/bin/python', '/var/www/html/LabelMe/Images/utils/prediction_overlay.py','original_images', $image );

my $redirect_url  = "http://localhost/LabelMe/tool.html?collection=LabelMe&mode=f&folder=overlayed_images_for_scribbles"."&image=$image";

print "Content-type: application/json\n\n";
my $response->{'redirect_url'} = $redirect_url;
$response->{'curr_dir'} = $script;
my $json_response = JSON::to_json($response);
print $json_response;
