#!/usr/bin/perl -w

use strict;
use File::Copy qw(copy);
use Image::Magick;
use File::Compare;

my $src_dir = "./icons_src";
my $dst_dir = "./icons";

sub normalize_filename
{
    my $icon_filename = $_[0];
    my $normalized_filename = lc($icon_filename);
    $normalized_filename =~ s/[^A-Za-z0-9\.]/_/g;
    $normalized_filename =~ s/_+/_/g;
    printf('%s -> %s'."\n", $icon_filename, $normalized_filename);
    return $normalized_filename;
}

sub im_convert_size
{
    my ($src_file, $dst_file, $dim) = @_[0..2];
    my $image = Image::Magick->new();
    $image->Read($src_file);
    $image->Resize(geometry => sprintf("%sx%s", $dim, $dim));
    $image->Write(filename => $dst_file);
}

sub convert_and_store
{
    my ($icon_filename, $normalized_filename) = @_[0..1];
    my $src = sprintf('%s/%s', $src_dir, $icon_filename);
    my $dst_64 = sprintf('%s/64/%s', $dst_dir, $normalized_filename);
    my $dst_32 = sprintf('%s/32/%s', $dst_dir, $normalized_filename);
    my $dst_16 = sprintf('%s/16/%s', $dst_dir, $normalized_filename);
    if ( not -f $dst_64 or compare($src, $dst_64) != 0 )
    {
        copy($src, $dst_64);
    }
    if ( not -f $dst_32 )
    {
        im_convert_size($src, $dst_32, 32);
    }
    if ( not -f $dst_16 )
    {
        im_convert_size($src, $dst_16, 16);
    }
}

opendir (DIR, $src_dir) or die $!;
while (my $icon_filename = readdir(DIR))
{
    next if ($icon_filename =~ m/^\./);
    convert_and_store($icon_filename, normalize_filename($icon_filename));
}
