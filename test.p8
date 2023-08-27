pico-8 cartridge // http://www.pico-8.com
version 41
__lua__

--[[
By Jaden Speth
]]--
-- compressed image input
input = "[0>2639:2>34:1>90:4>33:1>89:6>122:5>123:6>121:7>119:10>116:17>110:18>110:3>1:13>116:11>117:11>118:9>118:9>119:8>119:9>4:1>115:8>2:3>115:13>115:12>117:11>117:17>112:17>110:19>109:22>105:21>106:24>103:23>104:2>1:22>101:27>102:26>103:25>102:1>2:6>2:14>1:1>45:1>58:1>1:4>3:10>1:3>46:2>60:2>4:3>1:8>48:1>61:2>4:4>2:2>52:1>61:2>4:4>3:1>50:4>67:2>54:7>122:5>123:5>123:5>123:5>120:10>116:15>113:15>8:1>27:2>74:16>8:1>27:2>74:17>6:3>25:4>73:17>5:5>23:6>72:16>6:5>23:6>72:16>5:7>22:6>72:16>5:7>22:6>72:16>5:7>22:6>72:16>5:7>22:6>72:16>5:7>22:6>72:16>5:10>19:6>72:16>5:25>4:6>64:55>3:6>64:56>2:6>64:57>1:6>64:64>64:64>64:64>64:64>64:64>64:64>64:64>64:64>64:64>64:64>64:64>64:64>64:64>64:64>64:64>64:64>64:64]"

-- vars to update later
b_x,b_y,b_c = 0,0,7


function _init()
    -- var setup
    index = 1
    -- extract the bg color, set screen accordingly
    -- dont need the first char, discard
    input = sub(input, 2)
    -- now we can get the bg bit
    bg = input[1]
    -- now throw away the bit
    input = sub(input, 2)
    -- fix bg color
    if bg == 1 then
        -- change to white
        bg = 7
    end

    --
    -- decompression and drawing
    --

    -- set "brush" positions and color
    b_x = 0
    b_y = 0


    -- brush color is inverse of bg color
    if bg ~= 0 then
        -- black, so pick white
        b_c = 7
    else
        -- white, so pick black
        b_c = 0
    end
end

-- drawing and skipping function

function draw_skip(skip,draw_num)
    -- skip is a bool
    -- draw_num is... a num
    if skip then
        -- calculate new brush position
        -- convert to a total offset
        total = (b_x + (b_y * 128))
        -- add skip amount
        total += draw_num
        -- convert back into x/y
        b_x = total % 128 -- remainder fun
        b_y = flr(total/128)
        -- done!
        return
    else
        -- drawing pixels! oh fun!
        while draw_num > 0 do
            -- check cursor alignment
            if b_x > 127 then
                -- snap back and inc
                b_x = 0
                b_y += 1
            end
            -- draw a pixel at cursor pos
            pset(b_x, b_y, b_c)
            -- move the brush
            b_x += 1
            -- decrement draw_num
            draw_num += -1
        end
        -- all pixels are drawn!
    end
    -- skips or draws done!
end


-- parse and draw!
function decompress_n_draw()
    -- clear the screen
    cls(bg)
    -- # is the length operator
    while #input > 0 do
        if input[1] == "]" then
            -- dont care about closing bracket!
            input = sub(input, 2)
            goto cont
        end
        if (input[1] == ">" or input[1] == ":") then
            -- time to count pixels!
            -- lets find out how many.
            iter = 2
            while true do
                if input[iter] ~= ">" and input[iter] ~= ":" and input[iter] ~= "]" then
                    -- its a number! add to iter
                    iter += 1
                else
                    -- NAN! break!
                    break
                end
            end
            -- now we know how long the number is, extract it.
            number = tonum(sub(input,2,iter-1))
            -- do we need to draw or skip?
            if input[1] == ">" then
                --skip!
                draw_skip(true, number)
            else
                -- now draw it!
                draw_skip(false, number)
            end
            -- done! now we need to remove the operator and number
            input = sub(input, iter)
            -- done!
            goto cont
        end
        ::cont::
    end
    -- full thing should be drawn now!
end
function _update()
    decompress_n_draw()
    stop("done")
end