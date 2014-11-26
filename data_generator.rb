#DATA GENERATOR

class DataGenerator
	class << self
		def generate
			file = File.new("input200.csv", "w")
			for i in 0..100
			    players = [
                    '-9T','-8T','-7T','-6T','-5T','-4T','-3T','-2T','-1T','+1T','+2T','+3T','+4T','+5T','+6T','+7T','+8T','+9T',
                    '-9L','-8L','-7L','-6L','-5L','-4L','-3L','-2L','-1L','+1L','+2L','+3L','+4L','+5L','+6L','+7L','+8L','+9L',
                    '+5W','+5W','+5W','+5W'
                ].shuffle
                file.puts(players.join(","))
			end
		end
	end
end

DataGenerator.generate
