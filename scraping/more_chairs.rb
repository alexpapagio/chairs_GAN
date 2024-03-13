require 'capybara'
require 'capybara/dsl'

# Configure Capybara to use the desired driver
Capybara.default_driver = :selenium_chrome

# let's not make it too obvious & public which site
TARGET = ENV['TARGET']
MAX_PAGES = 100

# Define a new class for your script
class MoreChairsScraper
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

    # wait for loading
    page.first('figure[data-cy="resource-thumbnail"] img[data-nimg][src]', wait: 10)

    img_n = 0

    failed = []

    1.upto(MAX_PAGES) do |n|
      puts "Scraping page #{n} of #{MAX_PAGES}"
      puts page.current_url

      sleep(2 + rand(3)) # Add a random sleep to try to look human; it's going to be the wrong kind of random vs a human, but better than almost constant delay

      # screenshot the page state for debugging
      page.save_screenshot("raw_data/scraped-more/page-#{n}.png")

      # Find all the desired elements using a more specific CSS selector
      elements = all('figure[data-cy="resource-thumbnail"] img[data-nimg][src]')

      if elements.empty?
        puts "No more images found"
        page.save_screenshot("raw_data/scraped-more/final-page-#{n}.png")
        break
      end

      # Extract the source URLs of the images and convert them to Data URLs
      elements.each do |element|
        img_n += 1
        src = element['src']

        if src && src.match?(/^http/)
          # remove the querystring (? and after) from the src string
          src = src.match(/^[^\?]+/)[0]
          filename = src.split('/').last
          filename.gsub!(/\.jpg\z/, "")
          filename.gsub!(/\.jpeg\z/, "")
          filename.gsub!(/\.gif\z/, "")
          filename.gsub!(/\.png\z/, "")
          filename.gsub!(/\.webp\z/, "")

          puts "reading data from image #{img_n}"

          begin
            # if file does not already exist
            target_file_path = "raw_data/scraped-more/#{filename}.jpg"
            if File.exist?(target_file_path)
              puts "file already exists, skipping: #{target_file_path}"
              next
            end

            data_url = get_data_url(src) # Assuming get_data_url is a method that gets the data URL of an image

            # Extract the base64 data from the data URL
            base64_data = data_url.split(',')[1]

            # Decode the base64 data and write it to a file
            File.open(target_file_path, 'wb') do |f|
              f.write(Base64.decode64(base64_data))
            end
          rescue Selenium::WebDriver::Error::JavascriptError, Selenium::WebDriver::Error::ScriptTimeoutError
            puts "Failed to load image"
            failed << src
          end
        end
      end

      # Next page
      if (next_button = page.first("a[data-testid='pagination-next']", minimum: 0))
        next_button.click
      else
        puts "No more pages"
        break
      end

      File.write("raw_data/scraped-more/failed-#{Time.now.to_i}.txt", failed.join("\n")) if !failed.empty?
    end
  end
end

# Run the script
scraper = MoreChairsScraper.new
scraper.run