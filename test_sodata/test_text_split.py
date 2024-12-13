# -*- coding: utf-8 -*- 
# @File : test_text_split.py
# @Author : zh 
# @Time : 2024/4/16 下午2:17
# @Desc : 测试文本切分模块
import random

from sodata.text_split import BookSplitTool, ChineseRecursiveTextSplitter
from sodata.file_process import FileProcessTool

# # 1.测试custom_sampling采样函数
# import unittest  
# import random
# random.seed(42) 
# class TestCustomSampling(unittest.TestCase):  
#     # 测试边界值是否被选中  
#     def test_boundary_values(self):      
#         seg1, seg2, seg3, seg4 = 200, 1000, 2000, 4000  
#         p1, p2, p3 = 0.25, 0.25, 0.5   
#         for _ in range(100):  
#             sample = BookSplitTool.custom_sampling(seg1, seg2, seg3, seg4, p1, p2, p3)  
#             self.assertTrue(sample == seg1 or sample == seg2 or sample == seg3 or sample == seg4 or (seg1 < sample < seg4),  
#                             f"Sample {sample} is not a boundary value and not within the expected range")  
#     #测试抽样分布是否接近预期的概率分布
#     def test_custom_sampling_probabilities(self):  
#         seg1, seg2, seg3, seg4 = 200, 1000, 2000, 4000  
#         p1, p2, p3 = 0.25, 0.25, 0.5  
#         # 初始化计数器  
#         counts = [0, 0, 0]         
#         # 运行足够多的抽样以接近预期的概率分布  
#         num_samples = 100000  
#         for _ in range(num_samples):  
#             sample = BookSplitTool.custom_sampling(seg1, seg2, seg3, seg4, p1, p2, p3)  
#             if seg1 <= sample < seg2:  
#                 counts[0] += 1  
#             elif seg2 <= sample < seg3:  
#                 counts[1] += 1  
#             elif seg3 <= sample <= seg4:  
#                 counts[2] += 1  
#         # 计算实际概率并断言它们接近预期的概率  
#         actual_p1 = counts[0] / num_samples  
#         actual_p2 = counts[1] / num_samples  
#         actual_p3 = counts[2] / num_samples  
          
#         self.assertAlmostEqual(actual_p1, p1, delta=0.01)  
#         self.assertAlmostEqual(actual_p2, p2, delta=0.01)  
#         self.assertAlmostEqual(actual_p3, p3, delta=0.01)
# # 运行测试用例  
# unittest.main()


#2.测试convert_book_to_chunks--将一本书切分成多个文本块
# input_path = '/home/zhanghong/sodata/data/BL/墨香铜臭/《天官赐福》（精校版全本+番外完）作者：墨香铜臭.txt'
# text_data = FileProcessTool.process_txt_file(input_path)
# chunk_list, chunk_size = BookSplitTool.convert_book_to_chunks(text_data)
# print(len(max(chunk_list, key=len)), chunk_size)
# print(f"max_chunK:{repr(max(chunk_list,key = len))}, chunk_size:{chunk_size}")


# #3.测试split_text_into_head_tail--将文本chunk切分成头尾两部分
# chunk = '第50章 玲珑骰只为一人安 3\n\u3000\u3000按理说, 人是不会知道自己的背影是什么样子的, 然而，谢怜不同。他对自己的背影, 是再熟悉不过了。\n\u3000\u3000当年仙乐国破后, 人们为了泄愤, 烧了他八千太子殿，推倒了所有的太子像, 盗走剑柄宝石, 刮走衣上黄金。可他们仍然不解恨，于是, 有人逐渐想出了一种新花样, 那就是专门塑造这种跪地石像。\n\u3000\u3000把原先他们高高供奉起来的太子殿下塑成跪地认罪的姿势, 摆放在人流众多处，鼓吹走过去时冲这木木的石像吐一口唾沫或抽打两下就可以去除晦气。或者更进一步，直接塑成伏地磕头状，用以代替门槛, 供千人踩万人踏。在仙乐灭国后的一二十年里, 许多城镇与村庄都能看到这些石像, 谢怜又如何会不熟悉自己跪下来后的背影是什么样的？\n\u3000\u3000正在此时，一个年轻男子的声音道：“裴宿这条小癞狗抱着裴种马的狗腿才巴巴地上了天，还真以为自己有几斤几两？现在他不过就是条被流放的野狗，敢坏我的事，我教他被风干了也没人敢收尸！”\n\u3000\u3000人尚未至，骂声先至。谢怜侧目望去, 只见一个身形飘逸的青衫人走了进来。处于某种不值一提的原因，谢怜忍不住第一眼就去看了他的头顶，看到他戴着面具，头顶无灯，竟然微觉失望。一群青衣小鬼簇拥着这名青衣人，仿佛一圈蜡烛围着中间一个人。想必，这就是那传说中的鬼界四大害之一，青鬼戚容了。\n\u3000\u3000从南风第一次提到戚容的名字开始，谢怜就留了一丝意，想过这个“戚容”是不是他知道的那个戚容。但因为那个约定俗成的观念：妖魔鬼怪，都会隐瞒自己真实的名字，藏匿他们过往的人生，是以，他觉得可能并非同一人，只是假名重名了。然而如今看来，他倒有八九分把握了。因为，若不是他认识的那个戚容，怎么会有另一个戚容对那跪地太子像也这般执着？一开口，声音又怎会略为耳熟？\n\u3000\u3000那群青衣小鬼围着戚容高声呼王，七嘴八舌，谢怜听了大概。原来这戚容派了几个心腹去鬼市，闹事不成，给花城打得灰飞烟灭，于是他准备再战。谁知这第二轮还没放出去呢，就在路上遇到了被流放的裴宿。裴宿现在虽然被下放人间了，但好歹曾经是个神官，也没别的事干，遇上了便顺手清理了一波，于是又给打得灰飞烟灭。\n\u3000\u3000短短时间内连折两波心腹，戚容一得知消息便大发雷霆，诅咒连连：“有其祖必有其后，裴茗这匹下体生疮的狗种马，该要剁了他和裴宿的烂屌挂在他们庙前，谁拜他们谁就跟他们一样步步流脓！”\n\u3000\u3000谢怜听着，真有种捂住耳朵的冲动。同样是骂人，风信一激动，也骂得不堪入耳，可他骂得再难听，也能明显感觉出来他不过一时血气上涌，并无真实诅咒意图。而戚容的骂法则不然，让人听了毫不怀疑他心里是当真希望被他咒的人死得如他骂得那般肮脏龌龊，完全不吝攻人下三路，简直是下流了。\n\u3000\u3000那群青衣小鬼大声附和。戚容大概是想起了他一手提拔的得力下属，又道：“可惜了宣姬这么一个烈性的好女子，给这不要脸的裴家二狗逮住受了天大的委屈，到现在都救不出来！”\n\u3000\u3000谢怜听了，不敢苟同。纵是宣姬有可悲之处，但也不似他们说得这般仿佛全都是裴将军一人的错，毕竟那十几个新娘是她本人主动掳去的，也是她本人杀死的。烈性不假，好女子待商榷。而前面他骂小裴是抱着裴将军的大腿才飞升的，这一点谢怜更不敢苟同。这么多年上上下下过来，有一句话他是敢说的：有本事的，不一定能飞升；但飞升了的，就一定有他的本事。若自身无实力，再怎么求人提携，过不了那道天劫，最多也只得一个“同神官”凑合。谢怜与裴宿虽交集不多，但他能看出，小裴之武力，隐隐在郎千秋之上。只是，有多大本事也不等于就能有多高地位，运势也是要素之一，不然裴宿早就该单独立殿了。'
# head_text, tail_text = BookSplitTool.split_text_into_head_tail(chunk)
# print(f"head_text:{head_text}\ntail_text:{tail_text}")


# #4.测试convert_chunk_into_head_tail_seg--将一本书切分成多个文本块
# chunk = '第50章 玲珑骰只为一人安 3\n\u3000\u3000按理说, 人是不会知道自己的背影是什么样子的, 然而，谢怜不同。他对自己的背影, 是再熟悉不过了。\n\u3000\u3000当年仙乐国破后, 人们为了泄愤, 烧了他八千太子殿，推倒了所有的太子像, 盗走剑柄宝石, 刮走衣上黄金。可他们仍然不解恨，于是, 有人逐渐想出了一种新花样, 那就是专门塑造这种跪地石像。\n\u3000\u3000把原先他们高高供奉起来的太子殿下塑成跪地认罪的姿势, 摆放在人流众多处，鼓吹走过去时冲这木木的石像吐一口唾沫或抽打两下就可以去除晦气。或者更进一步，直接塑成伏地磕头状，用以代替门槛, 供千人踩万人踏。在仙乐灭国后的一二十年里, 许多城镇与村庄都能看到这些石像, 谢怜又如何会不熟悉自己跪下来后的背影是什么样的？\n\u3000\u3000正在此时，一个年轻男子的声音道：“裴宿这条小癞狗抱着裴种马的狗腿才巴巴地上了天，还真以为自己有几斤几两？现在他不过就是条被流放的野狗，敢坏我的事，我教他被风干了也没人敢收尸！”\n\u3000\u3000人尚未至，骂声先至。谢怜侧目望去, 只见一个身形飘逸的青衫人走了进来。处于某种不值一提的原因，谢怜忍不住第一眼就去看了他的头顶，看到他戴着面具，头顶无灯，竟然微觉失望。一群青衣小鬼簇拥着这名青衣人，仿佛一圈蜡烛围着中间一个人。想必，这就是那传说中的鬼界四大害之一，青鬼戚容了。\n\u3000\u3000从南风第一次提到戚容的名字开始，谢怜就留了一丝意，想过这个“戚容”是不是他知道的那个戚容。但因为那个约定俗成的观念：妖魔鬼怪，都会隐瞒自己真实的名字，藏匿他们过往的人生，是以，他觉得可能并非同一人，只是假名重名了。然而如今看来，他倒有八九分把握了。因为，若不是他认识的那个戚容，怎么会有另一个戚容对那跪地太子像也这般执着？一开口，声音又怎会略为耳熟？\n\u3000\u3000那群青衣小鬼围着戚容高声呼王，七嘴八舌，谢怜听了大概。原来这戚容派了几个心腹去鬼市，闹事不成，给花城打得灰飞烟灭，于是他准备再战。谁知这第二轮还没放出去呢，就在路上遇到了被流放的裴宿。裴宿现在虽然被下放人间了，但好歹曾经是个神官，也没别的事干，遇上了便顺手清理了一波，于是又给打得灰飞烟灭。\n\u3000\u3000短短时间内连折两波心腹，戚容一得知消息便大发雷霆，诅咒连连：“有其祖必有其后，裴茗这匹下体生疮的狗种马，该要剁了他和裴宿的烂屌挂在他们庙前，谁拜他们谁就跟他们一样步步流脓！”\n\u3000\u3000谢怜听着，真有种捂住耳朵的冲动。同样是骂人，风信一激动，也骂得不堪入耳，可他骂得再难听，也能明显感觉出来他不过一时血气上涌，并无真实诅咒意图。而戚容的骂法则不然，让人听了毫不怀疑他心里是当真希望被他咒的人死得如他骂得那般肮脏龌龊，完全不吝攻人下三路，简直是下流了。\n\u3000\u3000那群青衣小鬼大声附和。戚容大概是想起了他一手提拔的得力下属，又道：“可惜了宣姬这么一个烈性的好女子，给这不要脸的裴家二狗逮住受了天大的委屈，到现在都救不出来！”\n\u3000\u3000谢怜听了，不敢苟同。纵是宣姬有可悲之处，但也不似他们说得这般仿佛全都是裴将军一人的错，毕竟那十几个新娘是她本人主动掳去的，也是她本人杀死的。烈性不假，好女子待商榷。而前面他骂小裴是抱着裴将军的大腿才飞升的，这一点谢怜更不敢苟同。这么多年上上下下过来，有一句话他是敢说的：有本事的，不一定能飞升；但飞升了的，就一定有他的本事。若自身无实力，再怎么求人提携，过不了那道天劫，最多也只得一个“同神官”凑合。谢怜与裴宿虽交集不多，但他能看出，小裴之武力，隐隐在郎千秋之上。只是，有多大本事也不等于就能有多高地位，运势也是要素之一，不然裴宿早就该单独立殿了。'
# chunk_size = 1479
# min_idx = 200
# max_idx = min(chunk_size, 1000)
# head_text, tail_text = BookSplitTool.convert_chunk_into_head_tail_seg(chunk,min_idx,max_idx,chunk_size)
# print(f"head_text:{head_text}\ntail_text:{tail_text}")


# # 5.测试convert_chunk_into_segments--将文本chunk切分成多个文本块落
# chunk = "前面稀稀拉拉的，都是一些小神官，长明灯从几盏到几十不等，大家都没什么兴趣。但是，越到后来，每一次升起灯时光芒越盛，大家也越发专注。如果不是专门的神官报幕，一眼就能看出数目，那灯阵密密麻麻一起飞上来根本数不完有多少盏。谢怜什么都不清楚，便什么评价都不发表，专心欣赏明灯照亮漆黑长夜的美景，顺便听一听其他人对于目前斗灯形势的分析。虽然他觉得这种事情并没什么好分析的。大约两炷香后，压轴戏终于陆续来临。中秋宴斗灯，开始了最后的十甲拼杀。\n\u3000\u3000十甲的最后一名，谢怜听到报幕神官高声道：“奇英殿，四百二十一盏！”\n\u3000\u3000权一真早已离场了，其他神官听到这个数目后的啧啧之声也就不加掩饰了。这位西方武神年纪尚轻，却势头极猛，和他资历相同的神官，有两百盏长明灯已经算很多了，他却是翻了个倍还要多，飞升年限比他略长的郎千秋长明灯却比他略少，可谓了得。但谢怜觉得，果然这少年在上天庭人缘不太好，因为除了他自己和师青玄，几乎没什么为这份了得真心惊叹。\n\u3000\u3000下一位，地师殿，四百四十四盏。明仪除了多喝了两口汤，并没有任何别的表示，师青玄却是比他还激动，一叠声地道“低了低了”。由于大家对地师大人都不是很熟，章程化地拍了拍手，就当是祝贺了。紧接着就轮到师青玄自己了，风师殿，五百二十三盏。\n\u3000\u3000一个人受不受欢迎，真是很容易看出来的一件事。报出风师殿的长明灯数目后，师青玄还没说话，宴席上的抚掌声便陡然大了起来，四处都是“恭喜恭喜”“实至名归”。师青玄十分得意，起身到处拱手，又对师无渡嚷道：“哥，我今年第八！”\n\u3000\u3000他像被夫子夸了找爹妈讨赏似的，谢怜看着忍俊不禁，师无渡却斥道：“不过是第八而已，有什么好高兴的！”\n\u3000\u3000他这话其实是非常狂妄的。整个上天庭，有哪个是等闲之辈？五百盏长明灯，高居第八，在他口里却被说成“不过是”，那排在第八名后面的神官，岂不是连“而已”都不如？他也并非不知此话不妥，但他就是要这么说，因为不惧。师青玄垮了脸，师无渡摇了摇扇子，又勉为其难地道：“不过，灯比去年多了，下一年必须更多。”\n\u3000\u3000闻言，师青玄又纵臂长笑起来。整个宴席上，竟然只有明仪一脸漠然地埋头吃饭，不给他喝彩，于是师青玄拍了他两下，要找他讨祝贺。明仪根本不想理他，继续专心猛吃，师青玄大怒，要求他必须给自己鼓掌，谢怜在一旁听得要笑岔气了，不提。\n\u3000\u3000下一位，灵文殿，五百三十六盏。\n\u3000\u3000在文神里，灵文算是夺魁了，不过，并没有多少文神捧场，反倒主要是武神们很给面子。谢怜远远向他道了恭喜，这头听到师无渡和裴茗叫他摆宴请客，那头又听到有神官嘀咕，灵文信徒多无非是因为化了男相、灵文看准当今武神势大便一力巴结武神不理睬文神、灵文是上天庭最热衷于请客的神官、灵文据说有时请客还请嫖云云，摇了摇头，心中只有一个想法：女神官真不容易。\n\u3000\u3000接下来，是南阳殿和玄真殿，分别是五百七十二盏，和五百七十三盏。慕情眉目舒展，风信不喜不怒，似乎并不在意。谢怜心中纳闷，怎么会刚好数目这么接近？"
# segments = BookSplitTool.convert_chunk_into_segments(chunk,len_seg=50)
# #在用split_pattern分割后的句子后添加一个句号用于分隔不同句子
# print(segments)

# 6.测试convert_book_to_segment--将小说文本text切分成多个文本块落
# input_path = '/home/zhanghong/sodata/data/BL/墨香铜臭/《天官赐福》（精校版全本+番外完）作者：墨香铜臭.txt'
# text_data = FileProcessTool.process_txt_file(input_path)
# segments = BookSplitTool.convert_book_to_segment(text_data,chunk_sample = False)
# print(f"min_segmnets:{min(segments[0],key = len)}, segmnets_len:{len(segments)}")
# min_segment = min((segment for sublist in segments for segment in sublist if isinstance(segment, str)), key=len)  
# print(f"min_segment:{min_segment}, segments_len:{len(segments)}")
# print(f"segments:{segments}")


# # 7.测试split_text_into_HT_by_ratio--按照比例切分文本chunk
# chunk = "第50章 玲珑骰只为一人安 3\n\u3000\u3000按理说, 人是不会知道自己的背影是什么样子的, 然而，谢怜不同。他对自己的背影, 是再熟悉不过了。\n\u3000\u3000当年仙乐国破后, 人们为了泄愤, 烧了他八千太子殿，推倒了所有的太子像, 盗走剑柄宝石, 刮走衣上黄金。可他们仍然不解恨，于是, 有人逐渐想出了一种新花样, 那就是专门塑造这种跪地石像。\n\u3000\u3000把原先他们高高供奉起来的太子殿下塑成跪地认罪的姿势, 摆放在人流众多处，鼓吹走过去时冲这木木的石像吐一口唾沫或抽打两下就可以去除晦气。或者更进一步，直接塑成伏地磕头状，用以代替门槛, 供千人踩万人踏。在仙乐灭国后的一二十年里, 许多城镇与村庄都能看到这些石像, 谢怜又如何会不熟悉自己跪下来后的背影是什么样的？\n\u3000\u3000正在此时，一个年轻男子的声音道：“裴宿这条小癞狗抱着裴种马的狗腿才巴巴地上了天，还真以"
# head_text, tail_text = BookSplitTool.split_text_into_HT_by_ratio(chunk)
# print(f"head_text Length:{len(head_text)}\ntail_text Length:{len(tail_text)}")

# # 8.测试convert_book_to_fixed_length_chunks--按照固定长度切分文本chunk，并将chunk块进行预处理，便于训练序列标注模型
# input_path = '/home/zhanghong/sodata/data/BL/墨香铜臭/《天官赐福》（精校版全本+番外完）作者：墨香铜臭.txt'
# text_data = FileProcessTool.process_txt_file(input_path)
# chunk_list, chunk_size = BookSplitTool.convert_book_to_fixed_length_chunks(text_data)
# max_length = max(len(s) for s in chunk_list)
# print(f"max_chunk:{max_length}, chunk_size:{chunk_size}")

# # 9.测试convert_book_to_fixed_length_chunks_and_add_noise--按照固定长度切分文本chunk，并向预处理后的chunk块添加噪声
# input_path = '/home/zhanghong/sodata/data/BL/墨香铜臭/《天官赐福》（精校版全本+番外完）作者：墨香铜臭.txt'
# text_data = FileProcessTool.process_txt_file(input_path)
#
# chunk_list , chunk_size = BookSplitTool.convert_book_to_fixed_length_chunks_and_add_noise(text_data)
# print(f"chunk_text:{random.choice(chunk_list)}, chunk_size:{chunk_size}")