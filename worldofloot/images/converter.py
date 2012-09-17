import boto
import cStringIO
import urllib
import Image

class ImageHandler():
  def __init__(self, bucket_name):
    self.bucket = bucket_name

  def resize_and_upload(self, url, target_filename, width, height):
    #Retrieve our source image from a URL
    fp = urllib.urlopen(url)

    #Load the URL data into an image
    img = cStringIO.StringIO(fp.read())
    im = Image.open(img)

    #Resize the image
    #im2 = im.resize((500, 100), Image.NEAREST)
    im.thumbnail((width, height), Image.ANTIALIAS)

    #we're saving the image into a cStringIO object to avoid writing to disk
    out_im2 = cStringIO.StringIO()
    #You MUST specify the file type because there is no file name to discern it from
    im.save(out_im2, 'JPEG')

    #Now we connect to our s3 bucket and upload from memory
    #credentials stored in environment AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
    conn = boto.connect_s3()

    #Connect to bucket and create key
    b = conn.get_bucket(self.bucket)
    target_path = target_filename + '.jpg'
    k = b.new_key(target_path)

    #Note we're setting contents from the in-memory string provided by cStringIO
    k.set_contents_from_string(out_im2.getvalue(), headers={ \
        'Cache-Control': 'max-age=31556926',
        'Content-Type': 'image/jpeg',
    })
    k.set_acl("public-read")
    return 'https://s3.amazonaws.com/%s/%s' % (self.bucket, target_path)
