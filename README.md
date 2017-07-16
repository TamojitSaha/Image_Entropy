# Image Entropy
## Calculating Image entropy using Python 2.7
The entropy of an image can be calculated by calculating at each pixel position (i,j) the entropy of the pixel-values within a 2-dim region centered at (i,j). In the following example the entropy of a grey-scale image is calculated and plotted. The region size is configured to be (2N x 2N) = (10,10).

### Sample usage

``` python
imageEntropy('lena.tiff', "Entropy in 10 x 10 neighbourhood", 10, 8, 600)
```
function format: imageEntropy(file_name, image_caption, image_height, image_width, DPI)


### Screenshot from Spyder IDE(Python 2.7)
![alt text](https://github.com/tamsaha1995/Image-Entropy-/blob/master/Screenshot.png "Screenshot.png")


### Source Image
![alt text](https://github.com/tamsaha1995/Image-Entropy-/blob/master/tagore.jpg "tagore.jpg")


### Entropy of the Source Image
![alt text](https://github.com/tamsaha1995/Image-Entropy-/blob/master/entropy_tagore.jpg "entropy_tagore.jpg")

