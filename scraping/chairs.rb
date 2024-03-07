require 'capybara'
require 'capybara/dsl'

# Configure Capybara to use the desired driver
Capybara.default_driver = :selenium_chrome

# let's not make it too obvious & public which site
TARGET = ENV['TARGET']
MAX_PAGES = 100

# Define a new class for your script
class ChairScraper
  include Capybara::DSL

  def run
    scrape_chairs
  end

  def get_data_url(src)
    page.evaluate_script(<<~JS)
      await new Promise((resolve, reject) => {
        var img = new Image();
        img.crossOrigin = 'anonymous';
        img.onload = function() {
          var canvas = document.createElement('canvas');
          canvas.width = this.width;
          canvas.height = this.height;
          var ctx = canvas.getContext('2d');
          ctx.drawImage(this, 0, 0);
          resolve(canvas.toDataURL('image/jpeg'));
        };
        img.onerror = function() {
          reject(new Error('Failed to load image'));
        };
        img.src = '#{src}';
      });
    JS
  end

  def scrape_chairs
    visit TARGET # Replace with the URL of the page you want to scrape

    page.find("div[data-test='search-photos-route']").click_on("Load more")

    img_n = 0

    1.upto(MAX_PAGES) do |n|
      puts "Scraping page #{n} of #{MAX_PAGES}"

      sleep(2 + rand(3)) # Add a random sleep to try to look human; it's going to be the wrong kind of random vs a human, but better than almost constant delay

      # screenshot the page state for debugging
      page.save_screenshot("raw_data/scraped/first-page-#{n}.png")

      # Find all the desired elements using a more specific CSS selector
      elements = all('figure[itemprop="image"] img[data-test="photo-grid-masonry-img"]')

      if elements.empty?
        puts "No more images found"
        page.save_screenshot("raw_data/scraped/final-page-#{n}.png")
        break
      end

      # Extract the source URLs of the images and convert them to Data URLs
      elements.each do |element|
        img_n += 1
        src = element['src']
        if src && src.match?(/^http/)
          puts "reading data from image #{img_n}"
          data_url = get_data_url(src) # Assuming get_data_url is a method that gets the data URL of an image

          # Extract the base64 data from the data URL
          base64_data = data_url.split(',')[1]

          # Decode the base64 data and write it to a file
          File.open("raw_data/scraped/image#{img_n}.jpg", 'wb') do |f|
            f.write(Base64.decode64(base64_data))
          end
        end
      end

      # To save memory vs infinite scroll, delete the seen image elements from the DOM
      elements.each do |element|
        page.execute_script('arguments[0].closest(\'figure[itemprop="image"]\').remove();', element.native)
      end

      # Scroll to the bottom of the page
      page.execute_script('window.scrollTo({left: 0, top: document.body.scrollHeight, behavior: "smooth"});')
    end
  end
end

# Run the script
scraper = ChairScraper.new
scraper.run