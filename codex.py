'''
**Steganographic Text Hiding**

This Python module embeds an ASCII string of any length into an RGB image and 
encrypts the information with a password.
'''
'''This part is for generating the ASCII coding'''

def hide(info):
    
    from binascii import hexlify
    from numpy import zeros
    
    input_information = info
    
    hex_data = hexlify(input_information)
    temp = zeros(len(hex_data)).astype('str')
    
    for i in range(len(hex_data)):
        temp[i] = hex_data[i]
        
    for j in range(len(temp)):    
        if temp[j] == '0': temp[j] = '0000'
        if temp[j] == '1': temp[j] = '0001'
        if temp[j] == '2': temp[j] = '0010'
        if temp[j] == '3': temp[j] = '0011'
        if temp[j] == '4': temp[j] = '0100'
        if temp[j] == '5': temp[j] = '0101'
        if temp[j] == '6': temp[j] = '0110'
        if temp[j] == '7': temp[j] = '0111'
        if temp[j] == '8': temp[j] = '1000'
        if temp[j] == '9': temp[j] = '1001'
        if temp[j] == 'a': temp[j] = '1010'
        if temp[j] == 'b': temp[j] = '1011'
        if temp[j] == 'c': temp[j] = '1100'
        if temp[j] == 'd': temp[j] = '1101'
        if temp[j] == 'e': temp[j] = '1110'
        if temp[j] == 'f': temp[j] = '1111'
    
    bin_out = zeros(4*len(temp)).astype('uint8')
    for i in range(len(temp)):
        for j in range(4):
            bin_out[4*i+j] = temp[i][j]
            
    return bin_out
    

def unhide(bindata):
    
    from binascii import unhexlify
    from numpy import zeros
    
    bin_data = bindata
    data = zeros(len(bin_data)/4).astype('str')
    
    for i in range(len(bin_data)/4):
        data[i] = 1000*bin_data[4*i]+100*bin_data[4*i+1]+10*bin_data[4*i+2]+bin_data[4*i+3]
    
    for j in range(len(data)):    
        if data[j] == '0'   : data[j] = '0'
        if data[j] == '1'   : data[j] = '1'
        if data[j] == '10'  : data[j] = '2' 
        if data[j] == '11'  : data[j] = '3' 
        if data[j] == '100' : data[j] = '4' 
        if data[j] == '101' : data[j] = '5' 
        if data[j] == '110' : data[j] = '6'
        if data[j] == '111' : data[j] = '7'
        if data[j] == '1000': data[j] = '8'
        if data[j] == '1001': data[j] = '9'
        if data[j] == '1010': data[j] = 'a'
        if data[j] == '1011': data[j] = 'b' 
        if data[j] == '1100': data[j] = 'c' 
        if data[j] == '1101': data[j] = 'd' 
        if data[j] == '1110': data[j] = 'e' 
        if data[j] == '1111': data[j] = 'f' 
        
    hex_string = ''
    
    for j in range(len(data)): 
        hex_string = hex_string + data[j]
    
    output_information = unhexlify(hex_string)
    return output_information
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

def lorenz(x, y, z, sigma=10., beta=8./3, rho=28.) :
  
    x_dot = sigma*(y-x)
    y_dot = x*(rho-z)-y
    z_dot = x*y-beta*z

    return x_dot, y_dot, z_dot    
    
def randgen(key, image_size):
    
    from numpy import zeros, remainder, uint8
    dt = 0.001
    n = image_size
    
    xs = zeros((n + 1,))
    ys = zeros((n + 1,))
    zs = zeros((n + 1,))
    
    xs[0], ys[0], zs[0] = key[0], key[1], key[2]
    
    for i in xrange(n) :

        x_dot, y_dot, z_dot = lorenz(xs[i], ys[i], zs[i])
        xs[i + 1] = xs[i] + (x_dot * dt)
        ys[i + 1] = ys[i] + (y_dot * dt)
        zs[i + 1] = zs[i] + (z_dot * dt)
        
    Xs =  remainder(abs(xs*10**14), 2).astype(uint8)
    Ys =  remainder(abs(ys*10**14), 2).astype(uint8)
    Zs =  remainder(abs(zs*10**14), 2).astype(uint8)
    
    rand_array = Xs ^ Ys ^ Zs
    
    return rand_array
    
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
    
'''This is to generate the stegoimage''' 
   
def encode(file_name, message, password, channel=None):
    '''
    This codes an ASCII string into the LSB plane of an RGB image.
    
    **Sample usage**:
    
    encode('love.tiff', 'I am the best!', [0.5, 1.5, 2], channel='R')
    
    encode('love.tiff', 'This is it<>?1233445566~!@#$%^&&*', [0.1, 2, -3])
    '''
    import os
    from numpy import zeros_like, uint8, bitwise_and, shape, append, zeros, reshape
    from numpy.random import randint
    from matplotlib.pyplot import imread, imsave
        
    image = imread(file_name)
    base = os.path.basename(file_name)
    name = os.path.splitext(base)[0]
    ext = os.path.splitext(base)[1]
    m, n, p = shape(image)
    
    image_data = image[:,:, 0:3]
    lsbp = zeros_like(image_data, dtype = uint8)
    lsbp[:] = 254  
    image_lsbp_cleared = bitwise_and(image_data, lsbp)
    
    bin_code_dummy = hide(message)
    code_length = len(bin_code_dummy)
    
    if          code_length < 10    : code_size = '0000' + str(code_length)
    if 10    <= code_length < 100   : code_size = '000'  + str(code_length)
    if 100   <= code_length < 1000  : code_size = '00'   + str(code_length)    
    if 1000  <= code_length < 10000 : code_size = '0'    + str(code_length)
    if 10000 <= code_length < 100000: code_size =          str(code_length)
    
    bin_code = hide(code_size + message)
    code_length = len(bin_code)
    
    if code_length >= m*n:
        'The image is too small to carry the entire message.' 
        'Try again with a larger image or less amount of text.'    
        
    elif code_length < m*n:
        bin_code_unencrypted = append(bin_code, zeros(m*n - code_length))
        bin_code = bin_code_unencrypted.astype(uint8) ^ randgen(password, m*n-1)
        
        if   channel == 'R':    
            image_r = image_lsbp_cleared[:, :, 0] + bin_code.reshape(m, n)
            image_g = image_lsbp_cleared[:, :, 1] + randint(0, 2, m*n).reshape(m, n)
            image_b = image_lsbp_cleared[:, :, 2] + randint(0, 2, m*n).reshape(m, n)
            
        elif channel == 'G':
            image_r = image_lsbp_cleared[:, :, 0] + randint(0, 2, m*n).reshape(m, n) 
            image_g = image_lsbp_cleared[:, :, 1] + bin_code.reshape(m, n)
            image_b = image_lsbp_cleared[:, :, 2] + randint(0, 2, m*n).reshape(m, n)
            
        elif channel == 'B':
            image_r = image_lsbp_cleared[:, :, 0] + randint(0, 2, m*n).reshape(m, n) 
            image_g = image_lsbp_cleared[:, :, 1] + randint(0, 2, m*n).reshape(m, n)
            image_b = image_lsbp_cleared[:, :, 2] + bin_code.reshape(m, n)
        
        else:
            image_r = image_lsbp_cleared[:, :, 0] + bin_code.reshape(m, n)
            image_g = image_lsbp_cleared[:, :, 1] + randint(0, 2, m*n).reshape(m, n)
            image_b = image_lsbp_cleared[:, :, 2] + randint(0, 2, m*n).reshape(m, n) 
        
    
        output_image = zeros_like(image, dtype = uint8)
        
        output_image[:, :, 0] = image_r 
        output_image[:, :, 1] = image_g   
        output_image[:, :, 2] = image_b   
        output_image[:, :, 3] = 255
    new_file_name = "coded_"+name+ext
    print "\nThe modified filename is: " + new_file_name
    imsave(new_file_name, output_image)
    
    
def decode(file_name, password, channel=None):
    
    '''
    This decodes the ASCII string embedded into the LSB plane of an RGB image.
    
    **Sample usage**:
    
    decode('coded_image.tiff', [0.5, 1.5, 2], channel='R')
    
    decode('coded_image.tiff', [0.1, 2, -3])
    '''
    
    from numpy import  uint8, bitwise_and, shape, ones
    from matplotlib.pyplot import imread
        
    image = imread(file_name)
    m, n, p = shape(image)
    
    decoder = ones((1,m*n), dtype = uint8)
        
    if   channel == 'R': message = image[:, :, 0].reshape(1, m*n)        
    elif channel == 'G': message = image[:, :, 1].reshape(1, m*n)        
    elif channel == 'B': message = image[:, :, 2].reshape(1, m*n)
    
    else: message = image[:, :, 0].reshape(1, m*n)
        
    message_plane_full = bitwise_and(message, decoder) ^ randgen(password, m*n-1)
    
    stop = int(unhide(message_plane_full[0, 0:40]))
    
    message_plane = message_plane_full[0, 40:stop+40]
    
    output_text = unhide(message_plane)

    return output_text