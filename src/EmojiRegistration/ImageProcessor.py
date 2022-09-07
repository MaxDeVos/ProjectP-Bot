import cv2


class ImageProcessor:

    imageState = None

    def __init__(self, image, name):
        self.emojiDim = 128
        self.original_name = name
        self.name = "images/" + name + "_proposed"
        self.image = image
        if image.height <= self.emojiDim and image.width <= self.emojiDim:
            self.image_state = "fit"
        elif image.height is image.width:
            self.image_state = "square"
        else:
            self.image_state = "bad"

    def get_image_state(self):
        return self.imageState

    async def downscale(self):
        await self.download_image()
        self.img = cv2.imread(self.name + ".png", -1)
        self.img = cv2.resize(self.img, (self.emojiDim, self.emojiDim), interpolation=cv2.INTER_AREA)
        cv2.imwrite(self.name + ".png", self.img)
        is_success, im_buf_arr = cv2.imencode(".png", self.img)
        self.bytes = im_buf_arr.tobytes()

    async def download_image(self):
        self.mat = await self.image.save(self.name + ".png")

    async def downscale_skew(self):
        await self.download_image()
        self.img = cv2.imread(self.name + ".png", -1)
        width = self.img.shape[1]
        height = self.img.shape[0]
        if width == height:
            width = self.emojiDim
            height = self.emojiDim
        elif width > height:
            ratio = height / width
            height = int(self.emojiDim * ratio)
            width = self.emojiDim
        else:
            ratio = width / height
            width = int(self.emojiDim * ratio)
            height = self.emojiDim
        self.img = cv2.resize(self.img, (width, height), interpolation=cv2.INTER_AREA)
        cv2.imwrite(self.name + ".png", self.img)
        is_success, im_buf_arr = cv2.imencode(".png", self.img)
        self.bytes = im_buf_arr.tobytes()
