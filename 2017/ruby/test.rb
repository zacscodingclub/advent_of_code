def test(description, result, expect)
  val = result == expect

  if val
    puts "#{description} - Test Passed"
  else
    puts "#{description} - Expected: #{expect},  Actual: #{result}"
  end
end
