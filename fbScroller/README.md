## Synopsis

This python scripts enalbes facebook wall to be scrollable using hand gestures.

## Code Example

if((y2-y1) > 60):
            print "Scroll Down"
            driver.execute_script("window.scrollTo("+str(i)+", "+str(end)+");")
            i = end
            end = end + 708
This module in the code scrolls the wall.

## Motivation

Facebook scrolling is a very common habit which we have. To reduce the pain of thumb or mouse scrolling, we can do this just waving our hand in the air. 

## Installation

You should have following modules install in your system:
Beautifulsoup
opencv 2 or 3

## How to run

python fb_scroller.py
