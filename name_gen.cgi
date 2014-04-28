#!/usr/bin/perl

#-------------------------------------------------------------------------
# Fantasy Name Generator
# By: Justin Rudler
# Verison: 0.1
# Create Date: 10/27/2010
# Description:
#-------------------------------------------------------------------------

use CGI qw/:standard/;

my %nametable;
my @racesexmenu;
my $name;
my $type;
my $number;
my @alpha = qw(a b c d e f g h i j k l m n o p q r s t u v w x y z);
my $alphalength = $#alpha;
my @prefix;
my $prefixlength;
my @suffix;
my $suffixlength;
my $restrict;
my $double;

# Load name format data
open (NAMEDATA, "namedata.csv") || die "Cannot open NAMEDATA";
while (<NAMEDATA>) {
	chomp;
    my ($race, $sex, $part, @data) = split /,/;
    $nametable{$race}{$sex}{$part} = [@data];
}
close NAMEDATA;

# Build menu item and values

foreach $race (sort keys %nametable) {
	foreach $sex (sort keys %{ $nametable{$race} } ) {
        push @racesexmenu, "$sex $race";
    }
}

# Web Page Generation

print
    header,
    start_html('Fantasy Name Generator'),
    h1('Fantasy Name Generator'),
    start_form,
    "Name Type: ",
    popup_menu(-name=>'type',-values=>\@racesexmenu),
    p,
    "Number Generated: ",
    popup_menu(-name=>'number',-values=>[1,10,25,50,100]),
    p,
    submit(-label=>'Create Names'),
    end_form,
    hr,"\n";

if (param) {

# Print name for each sex race combo
	$type = param('type');
	($sex, $race) = split(/ /, $type);
	@prefix = @{ $nametable{$race}{$sex}{prefix} };
	$prefixlength = $#prefix;
	@suffix = @{ $nametable{$race}{$sex}{suffix} };
	$suffixlength = $#suffix;
    $restrict = join('',@{ $nametable{$race}{$sex}{restrict} });
    $double = join('',@{ $nametable{$race}{$sex}{double} });
    $number = param('number');
    print "$type", p;
    while ($number > 0) {
    	$name ='';
		#random name length
		my $count = int(rand(2)+2);
		&prefix;
		while ($count >= 0) {
			if ($name =~ /[aeiouy]$/) {
		   		&consonant;
			} else {
				&vowel;
			}
    		$count--;
		}

		if ($name =~ /[aeiouy]$/) {
			&suffix;
		}

		# Capitalize the first letter of the name.
		$name =~ s/\b(\w)/\U$1/g;

		print "$name", p;
        $number--;
	}
#    print "Alpha: ", $alphalength, p;
#    print "Prefix: ", $prefixlength, p;
#    print "Suffix: ", $suffixlength, p;
}
print end_html;

sub prefix {
	my $x = int(rand($prefixlength));
    $name = ($name . $prefix[$x]);
}

sub consonant {
	CONSONANT: {
    	my $x = int(rand($alphalength));
    	my $y = $alpha[$x];
    	if ($y =~ /[aeiouy][$restrict]/) {
        	redo CONSONANT;
        } elsif ($y =~ /[$double]/) {
        	my $check = int(rand(100)+1);
            if ($check <= 20) {
            	$name = $name . $y . $y;
            } else {
            	$name = $name . $y;
            }
        }
    }
}

sub vowel {
	VOWEL: {
    	my $x = int(rand($alphalength));
    	my $y = $alpha[$x];
        if ($y =~ /[^aeiouy][$restrict]/) {
        	redo VOWEL;
        } else {
        	$name = $name . $y;
        }
    }
}

sub suffix {
	my $x = int(rand($suffixlength));
    $name = ($name . $suffix[$x]);
}
