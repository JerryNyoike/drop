const server = 'http://127.0.0.1:5000/';
const beat_request_limit = 30;
const beat_images = [
	"/static/assets/images/beat_img1.jpg",
	"/static/assets/images/beat_img2.jpg",
	"/static/assets/images/beat_img3.jpg",
	"/static/assets/images/beat_img4.jpg",
	"/static/assets/images/beat_img5.jpg",
	"/static/assets/images/beat_img6.jpg",
	"/static/assets/images/beat_img7.jpg",
	"/static/assets/images/beat_img8.jpg",
	"/static/assets/images/beat_img9.jpg",
	"/static/assets/images/beat_img10.jpg"
]
const photo_contributions = [
	{
		src: "\\static\\assets\\images\\home_stripe.jpg",
		credit: "Photo by Malte Wingen on Unsplash"
	},
	{
		src: "\\static\\assets\\images\\background_bg.jpg",
		credit: "Photo by Blaz Photo on Unsplash"
	},
	{
		src: "\\static\\assets\\images\\potrait1.jpg",
		credit: "Photo by Sašo Tušar on Unsplash"
	},
	{
		src: "\\static\\assets\\images\\potrait2.jpg",
		credit: "Photo by James Owen on Unsplash"
	},
	{
		src: "\\static\\assets\\images\\potrait3.jpg",
		credit: "Photo by Chris Yang on Unsplash"
	},
	{
		src: "\\static\\assets\\images\\beat_img1.jpg",
		credit: "Photo by Matthieu A on Unsplash"
	},
	{
		src: "\\static\\assets\\images\\beat_img2.jpg",
		credit: "Photo by Namroud Gorguis on Unsplash"
	},
	{
		src: "\\static\\assets\\images\\beat_img3.jpg",
		credit: "Photo by James Stamler on Unsplash"
	},
	{
		src: "\\static\\assets\\images\\beat_img4.jpg",
		credit: "Photo by MARK S. on Unsplash"
	},
	{
		src: "\\static\\assets\\images\\beat_img5.jpg",
		credit: "Photo by Paulo Infante on Unsplash"
	},
	{
		src: "\\static\\assets\\images\\beat_img6.jpg",
		credit: "Photo by Namroud Gorguis on Unsplash"
	},
	{
		src: "\\static\\assets\\images\\beat_img7.jpg",
		credit: "Photo by Eric Nopanen on Unsplash"
	},
	{
		src: "\\static\\assets\\images\\beat_img8.jpg",
		credit: "Photo by Eric Nopanen on Unsplash"
	},
	{
		src: "\\static\\assets\\images\\beat_img9.jpg",
		credit: "Photo by Kai Oberhäuser on Unsplash"
	},
	{
		src: "\\static\\assets\\images\\beat_img10.jpg",
		credit: "Photo by Travis Yewell on Unsplash"
	},
	{
		src: "\\static\\uploads\\photos\\producer.jpg",
		credit: "Photo by Tanner Boriack on Unsplash"
	},
	{
		src: "\\static\\assets\\images\\studio.jpg",
		credit: "Photo by Maxwell Hunt on Unsplash"
	},
	{
		src: "\\static\\assets\\images\\contact_banner.jpg",
		credit: "Photo by Adam Solomon on Unsplash"
	},
	{
		src: "\\static\\assets\\images\\about_banner.jpg",
		credit: "Photo by Art Lasovsky on Unsplash"
	}
];

function Beat(file, albumart, name, genre, leasePrice, sellingPrice, genres){
	this.file = file;
	this.albumart = albumart;
	this.name = name;
	this.genre = genre;
	this.leasePrice = leasePrice;
	this.sellingPrice = sellingPrice;
	this.genres = genre;
}

function Genre(){
	this.genre_id = genre_id;
	this.name = name;
}

function Preference(key, value){
	this.key = key;
	this.value = value;
}

