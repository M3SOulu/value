# coding: utf-8

from unipath import Path
import sys
import os

PROJECT_DIR = Path(os.path.abspath(__file__)).parent.parent
sys.path.append(PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'value.settings')

import django
django.setup()


import random
from django.utils import timezone
from value.deliverables.meetings.models import Meeting, Evaluation


def main(argv=sys.argv):
    if len(argv) > 1:
        meeting_id = argv[1]
        meeting = Meeting.objects.get(pk=meeting_id)
        meeting.evaluation_set.all().delete()

        measure = meeting.deliverable.measure
        measure_values = list(measure.measurevalue_set.all())

        pseudo_random_push = None
        if len(argv) > 2:
            pseudo_random_push = int(argv[2])

        true_random = [656, 868,279,150,101,616,1,853,658,564,251,71,991,458,804,116,568,582,929,464,693,409,122,941,334,476,273,257,8,27,850,402,693,144,636,187,924,0,215,555,346,227,254,70,574,709,972,552,889,406,814,648,915,954,924,43,968,43,149,593,15,160,779,414,710,613,0,341,110,645,991,529,857,794,952,250,993,921,617,503,619,690,810,921,50,723,297,5,577,535,165,921,529,696,444,909,587,186,447,706,393,65,760,615,979,71,83,471,587,17,878,935,670,315,339,840,826,85,622,639,263,757,919,203,761,248,455,398,139,121,222,335,444,652,405,991,323,233,274,129,635,548,400,402,561,566,453,246,971,683,736,427,105,828,334,24,285,872,295,706,649,138,64,502,319,760,6,24,282,375,727,984,92,166,695,792,611,130,539,335,754,417,944,328,390,100,143,187,722,859,975,584,825,738,256,873,261,26,237,444,277,801,8,44,532,275,765,765,339,844,340,800,784,485,326,992,314,53,260,11,109,536,916,484,852,183,265,902,225,207,867,737,696,353,266,377,286,251,420,979,942,181,700,782,391,139,749,194,249,106,75,127,910,920,949,181,258,811,928,12,272,151,850,168,556,505,186,381,354,633,265,506,262,579,317,78,964,837,643,268,90,898,816,759,555,946,823,623,221,1000,392,909,132,340,397,993,255,959,185,724,883,945,272,721,938,630,210,898,595,52,499,439,555,421,281,984,692,783,829,852,952,372,588,271,658,398,84,553,892,769,346,692,483,273,829,949,255,749,515,858,770,275,98,201,629,840,850,728,33,197,184,62,654,510,568,482,357,66,56,847,646,808,668,424,55,954,299,708,771,12,185,11,760,893,953,468,460,231,705,336,146,492,397,818,543,605,62,19,22,577,49,243,166,339,259,28,863,78,829,554,632,349,349,355,18,108,449,952,972,430,46,147,786,709,816,661,29,100,812,255,969,524,568,979,897,643,314,172,290,995,73,882,99,917,783,270,690,255,505,427,949,834,376,877,23,335,893,302,529,506,198,577,992,192,313,182,416,129,646,906,395,43,183,517,398,554,39,31,221,328,212,17,740,672,583,807,251,540,718,928,51,521,846,939,141,696,259,239,341,173,29,333,865,234,78,80,504,189,983,284,36,443,252,943,249,179,28,773,149,856,509,46,393,425,281,733,392,427,63,371,633,823,38,907,879,116,6,541,337,58,780,575,723,28,628,858,427,96,438,344,601,895,12,510,210,791,879,598,151,273,576,348,490,259,276,768,389,574,549,175,922,835,746,19,374,630,550,369,228,874,360,556,512,660,106,245,145,926,290,493,258,953,926,812,347,382,75,521,347,638,20,713,48,639,347,895,442,381,848,344,960,252,787,571,658,81,503,884,439,335,688,600,123,833,53,378,952,442,798,909,169,418,361,158,443,295,172,636,190,36,575,215,99,265,843,875,570,436,781,578,532,704,142,478,118,873,605,304,327,830,395,665,319,65,144,876,855,712,532,808,942,957,384,144,885,12,853,555,810,159,718,112,363,344,38,81,982,878,844,348,805,181,526,438,783,124,408,304,872,850,832,929,418,156,712,845,725,347,82,396,203,646,993,669,875,133,238,904,733,41,966,475,135,635,422,240,181,366,660,221,511,920,391,944,109,837,122,420,134,456,216,505,862,845,833,136,887,842,607,518,445,806,71,95,255,914,55,130,690,837,42,117,493,49,619,455,608,196,667,4,470,338,182,137,329,52,865,440,697,208,330,633,773,743,690,788,637,363,362,82,869,840,700,609,973,462,547,917,133,968,326,611,769,91,614,541,571,556,485,397,397,211,891,799,113,417,795,38,835,980,85,955,852,395,620,23,673,111,522,829,727,641,378,616,966,815,358,665,55,326,750,708,382,804,528,916,189,754,545,584,551,658,953,957,115,786,72,585,443,209,457,710,209,53,482,718,380,461,832,618,367,419,934,443,374,633,295,87,47,765,894,352,312,104,725,776,234,580,843,652,674,712,276,721,797,607,265,443,71,358,256,12,468,977,301,310,627,583,130,68,349,359,233,95,970,881,823,510,443,688,427,626,433,190,338,759,204,374,955,394,959,615,94,978,510,882,909,212,8,350,168,472,782,663,444,128,141,952,671,208,600,7,397,939,10,704,252,281,322,601,823,438,19,659,534,552,738,764,317,332,255,578,180,844,109,508,838,270,640,331,883,521,148,203,591,644,467,462,954,560,649,718,389,737,283,55,939,807,280,934,167,975,310,312,262,439,792,114,652,667,74,77,563,412,110,479,102,601,859,766,446,178,760,209,915,45,23,264,815,362,273,717,48,506,318,307,522,791,555,466,751,217,0,299,629,232,433,73,239,950,434,873,362,644,934,513,522,888,140,659,859,76,850,534,521,382,570,937,783,231,193,963,736,409,73,267,673,804,248,796,777,943,471,249,875,944,631,725,948,916,53,592,805,627,761,601,913,341,371,392,536,357,235,113,108,636,675,3,679,526,250,235,261,746,74,175,950,578,65,710,534,401,659,192,874,107,794,242,899,539,379,848,741,776,212,765,879,746,842,535,354,847,169,746,310,241,53,826,94,742,109,687,365,104,168,930,204,953,716,259,521,123,107,346,358,682,852,660,31,875,468,993,706,777,374,300,813,655,342,186,725,229,233,905,989,243,291,289,849,733,477,520,90,906,584,223,78,940,804,474,15,10,609,433,843,489,630,520,387,312,456,731,280,589,329,612,905,966,43,718,877,848,556,647,685,655,319,198,901,939,748,185,337,452,188,230,528,247,378,257,804,481,408,574,30,128,194,414,962,556,337,137,882,18,82,291,39,237,1,804,172,84,10,12,885,465,254,288,140,914,681,581,488,680,687,272,208,534,694,466,588,536,151,906,521,984,714,177,908,392,760,624,42,922,22,53,155,834,518,491,376,489,525,683,798,217,926,771,594,288,368,56,440,868,974,223,979,501,768,851,221,9,843,180,290,629,331,459,847,355,276,44,895,873,775,277,464,938,59,375,36,850,595,83,865,505,284,64,106,59,713,758,154,358,771,266,535,486,499,63,730,894,836,226,562,257,842,862,209,567,968,947,779,608,751,330,0,575,429,129,870,373,229,474,128,159,569,570,364,179,401,409,621,738,383,907,478,845,52,237,155,30,28,149,270,209,133,481,339,139,180,795,130,272,895,586,311,669,768,101,473,676,650,743,626,664,71,805,982,835,895,247,466,795,784,133,749,963,952,975,32,896,144,251,506,889,140,800,446,910,782,120,305,724,281,587,865,371,859,140,105,390,992,811,998,171,752,514,408,858,694,729,533,298,443,710,287,883,84,473,489,281,269,795,844,555,672,456,991,179,780,927,765,732,894,70,694,79,481,184,842,859,855,127,837,984,854,369,606,52,474,995,603,903,504,957,640,587,658,119,835,595,607,891,113,121,192,998,552,225,147,808,837,59,347,609,770,695,998,619,61,800,309,944,577,822,863,111,269,950,48,598,426,476,420,775,677,105,880,247,752,498,585,810,518,299,661,677,77,994,155,877,444,764,258,656,435,85,129,498,727,304,96,236,153,236,563,762,681,929,379,109,145,561,14,533,387,305,734,179,318,157,414,819,99,22,81,30,536,227,417,647,598,412,620,265,997,694,622,44,303,61,145,774,197,23,61,208,859,794,421,503,779,835,99,930,152,161,779,295,110,999,61,305,168,422,758,55,246,682,835,314,990,533,892,876,104,698,384,127,101,147,756,303,1,630,87,899,271,682,437,613,370,714,389,308,968,65,763,699,770,778,883,780,892,56,70,262,743,715,647,673,159,803,875,777,617,348,147,765,541,74,428,563,962,584,913,657,972,415,276,977,468,238,122,392,163,336,989,199,34,948,792,35,601,155,69,954,935,99,261,93,202,488,70,205,758,831,833,332,761,672,49,256,995,984,948,127,169,100,464,759,482,677,387,179,966,962,195,63,494,743,413,292,701,284,827,226,478,172,242,706,686,163,11,412,171,956,415,225,430,451,885,512,976,529,717,872,856,199,771,754,24,166,454,703,241,426,104,562,960,37,78,711,220,763,517,660,407,333,646,58,10,614,668,342,814,855,94,512,971,699,289,983,734,71,610,599,331,443,950,598,352,894,102,981,926,330,146,525,461,683,393,97,972,240,506,637,166,752,876,517,403,814,403,455,62,417,411,42,664,434,124,944,323,702,825,527,176,688,982,479,739,278,992,135,238,410,439,336,318,167,205,771,889,159,746,601,238,376,698,924,85,726,416,445,751,329,788,7,970,851,490,32,449,120,140,116,223,490,924,286,223,510,756,647,941,923,618,495,996,700,511,471,820,873,125,192,181,158,290,150,740,9,770,0,736,474,412,902,369,200,167,716,1000,129,757,954,75,755,604,711,525,69,454,986,154,649,718,658,970,957,381,107,848,396,219,440,992,678,664,624,192,846,820,263,323,335,796,103,627,175,165,739,591,964,92,543,448,332,220,737,543,139,714,111,908,901,445,515,302,8,84,116,868,857,501,132,317,784,96,258,265,2,661,546,959,186,332,837,480,788,959,102,529,522,649,475,532,914,116,971,395,167,140,46,825,556,737,347,750,834,115,75,371,976,233,738,447,482,826,92,121,127,648,654,352,361,293,358,507,378,643,778,444,65,564,265,889,149,603,27,4,8,298,69,685,982,864,163,352,40,948,295,960,286,399,611,416,683,291,390,678,107,760,698,34,180,838,985,329,660,509,26,391,730,973,648,583,720,48,91,311,105,742,844,861,346,50,956,773,203,517,185,844,298,678,214,332,678,643,30,392,124,27,841,460,618,765,532,303,645,813,176,595,965,420,986,538,78,476,868,171,24,234,100,972,638,681,969,322,28,262,777,816,517,285,521,834,683,677,200,177,959,867,211,861,376,181,246,855,288,552,673,549,732,643,595,829,705,273,114,978,494,896,72,670,671,476,554,114,546,696,427,863,38,392,687,946,806,174,502,193,924,690,724,319,263,891,715,694,1,714,501,675,558,59,638,129,451,551,139,11,357,100,664,217,334,414,591,710,750,319,68,85,563,542,624,659,758,195,624,309,611,49,81,297,633,635,822,755,16,151,574,277,579,715,209,660,237,643,624,38,366,922,267,569,160,163,597,716,151,67,505,766,99,185,444,652,827,904,949,568,889,396,22,199,288,799,443,358,165,377,224,678,446,206,980,711,589,439,162,1,226,976,742,350,245,347,666,455,678,310,788,328,704,605,79,164,767,338,439,102,822,213,398,24,23,189,574,886,542,93,815,374,687,798,247,999,223,470,460,921,704,916,379,544,54,581,112,709,800,213,5,840,866,32,716,532,213,41,692,907,399,285,444,578,826,954,371,500,180,930,773,80,986,127,184,377,416,754,187,602,836,125,566,519,770,758,203,361,872,955,203,545,959,54,190,399,60,531,228,353,361,109,946,384,678,583,645,798,196,806,746,51,310,101,6,405,388,969,639,40,577,537,960,55,771,704,348,153,398,541,717,512,788,24,556,173,914,983,596,669,488,537,198,264,525,910,121,499,840,449,343,176,341,401,465,269,428,369,125,672,226,496,178,796,489,78,473,910,9,615,754,310,801,262,264,331,664,915,894,674,177,410,743,458,563,709,839,729,659,629,156,129,463,881,138,306,122,728,928,881,974,531,553,400,279,972,305,526,156,818,34,577,979,143,176,446,640,346,287,26,909,223,49,868,647,314,776,763,268,717,242,641,925,96,77,578,951,116,780,801,685,898,945,840,241,68,308,512,611,208,552,31,285,68,120,522,52,183,114,702,107,207,766,626,341,624,482,267,721,507,728,900,903,916,51,252,655,649,778,579,578,304,7,424,962,783,198,407,391,704,991,748,933,941,574,557,304,608,199,924,260,9,243,64,770,984,551,75,135,340,91,226,207,589,713,155,377,600,959,337,748,281,715,342,765,264,911,647,430,500,988,694,944,112,1000,48,837,835,181,494,17,153,668,358,369,656,530,917,156,661,879,58,48,114,970,990,137,591,653,835,647,732,142,50,371,457,87,423,674,528,40,635,272,180,938,211,311,301,317,325,494,593,886,294,232,908,357,409,688,166,331,156,146,140,364,5,914,772,136,594,227,660,661,326,496,425,47,553,598,565,935,109,940,432,678,802,123,366,732,329,751,32,577,816,162,745,740,375,355,266,331,158,664,951,65,253,445,310,804,906,225,837,608,625,130,219,803,938,809,442,181,107,206,970,704,238,271,923,674,609,636,152,39,528,672,896,765,455,360,346,606,132,254,962,724,0,507,649,324,403,713,628,372,912,78,296,733,609,151,913,379,35,458,655,456,317,238,551,371,17,962,905,196,425,258,106,867,870,423,336,366,731,518,553,849,629,762,292,287,590,5,821,461,307,950,132,497,291,127,660,52,732,851,37,877,77,377,767,742,297,460,604,802,712,312,308,449,132,450,787,780,0,939,416,967,623,342,159,492,184,296,865,177,366,761,739,629,726,164,698,590,674,312,544,44,798,805,425,201,403,324,780,227,652,143,522,52,301,671,944,478,641,7,402,494,863,109,355,733,141,269,210,580,451,432,449,68,671,661,684,973,793,886,920,31,401,20,612,28,908,409,981,969,11,393,38,416,337,329,174,9,294,700,130,526,408,915,215,364,743,397,823,795,239,211,436,338,12,206,260,585,420,271,172,488,943,551,543,591,99,952,264,963,273,306,690,285,390,775,702,713,581,764,781,568,297,74,134,696,777,193,110,138,131,879,161,313,277,547,739,61,659,276,485,671,339,245,876,399,568,812,66,945,167,567,382,516,499,579,190,164,489,614,22,310,50,596,280,31,310,739,521,926,612,227,987,765,310,671,684,588,36,764,404,560,433,174,597,194,209,122,850,816,901,815,817,199,29,560,601,306,869,424,14,130,740,574,465,521,662,845,620,288,50,993,978,164,787,390,73,414,58,902,439,332,526,257,242,993,411,853,709,593,930,143,190,129,918,152,741,32,502,51,599,77,362,960,620,924,127,63,882,308,107,632,947,983,379,17,859,278,714,944,266,649,191,710,458,430,106,970,560,70,999,0,940,120,111,273,538,230,95,45,928,715,804,948,344,590,962,796,66,698,381,411,74,743,792,44,38,80,875,440,918,70,582,319,667,965,58,956,548,111,840,634,765,132,535,392,281,300,621,412,310,941,578,67,429,132,572,949,921,219,675,302,512,344,354,256,453,85,731,461,97,510,598,882,447,494,65,558,888,923,391,562,965,141,611,251,599,156,459,354,597,111,314,600,216,741,374,850,851,817,174,986,401,551,289,964,527,287,409,323,836,219,359,708,221,276,985,671,618,530,519,447,524,627,137,747,369,846,572,821,959,470,190,580,847,615,97,620,894,275,390,444,476,753,555,620,673,634,99,594,73,154,611,9,217,793,731,545,257,327,601,282,358,370,599,423,124,955,196,953,677,375,729,63,932,111,548,102,884,890,17,89,550,751,270,195,901,72,725,808,959,984,750,91,813,811,292,406,91,988,988,991,329,496,741,422,518,50,668,543,879,219,481,878,344,836,656,782,204,41,702,966,813,487,480,264,555,169,26,378,927,701,7,161,349,628,851,128,196,883,952,689,303,211,275,915,506,54,106,193,99,264,436,327,809,108,937,280,206,760,110,739,143,799,314,440,842,268,495,132,759,417,878,864,594,835,80,593,19,793,363,298,784,489,897,213,48,845,562,951,497,495,74,526,710,742,582,867,884,43,503,819,987,801,405,330,187,328,790,18,938,678,93,900,788,547,982,149,979,790,687,787,162,279,667,910,522,481,339,750,918,570,675,161,383,280,324,486,880,230,450,759,110,914,410,488,373,895,530,302,402,326,142,381,281,871,43,260,704,626,591,937,384,412,45,180,188,557,936,906,645,544,4,841,97,605,364,65,74,497,523,480,704,222,228,176,709,819,182,785,365,469,710,845,296,19,998,170,130,204,483,953,143,255,472,256,82,570,736,94,913,950,649,401,674,332,685,222,343,752,456,493,239,488,761,756,822,226,477,532,249,277,480,754,233,997,857,852,807,122,968,458,508,130,862,473,601,798,337,852,338,4,534,687,614,665,635,359,150,921,626,239,66,433,842,768,433,294,129,623,60,217,362,370,176,311,998,75,986,957,904,326,368,632,733,159,228,16,280,23,560,600,837,805,25,246,653,59,773,625,870,419,444,842,38,958,138,295,508,998,500,222,681,401,560,15,36,779,961,878,33,212,857,947,862,94,183,256,658,750,788,419,133,191,168,736,580,621,807,205,172,440,440,322,500,971,644,809,162,229,486,572,884,590,421,509,916,367,383,654,433,239,217,191,278,9,633,575,373,34,112,600,216,183,586,991,944,72,210,738,901,63,917,643,179,11,883,990,547,363,376,128,476,158,208,508,125,887,286,368,691,268,802,135,487,601,178,243,427,162,339,975,982,283,31,814,873,896,339,653,393,200,650,358,494,333,928,123,358,357,719,180,289,329,193,908,854,371,347,273,886,608,682,374,261,954,345,787,890,322,267,517,737,776,780,935,998,238,268,398,33,471,514,826,307,689,596,784,852,435,775,697,176,49,379,556,48,617,116,197,246,144,224,249,667,702,970,448,269,693,785,672,347,514,822,407,69,368,251,929,318,628,18,526,450,144,511,974,741,969,616,908,556,867,763,317,576,124,16,911,511,350,919,752,133,850,288,803,410,876,823,112,202,195,896,614,254,830,733,97,241,656,631,939,66,158,317,925,56,334,174,820,293,583,781,18,337,524,474,471,732,574,724,767,996,428,41,624,725,389,724,339,240,457,264,937,917,279,58,194,519,307,402,808,812,525,500,785,810,562,864,690,995,258,746,784,917,290,566,412,614,883,70,404,412,298,604,541,71,669,64,262,708,990,166,182,162,727,278,252,293,167,176,452,427,284,438,117,289,686,886,981,446,206,168,679,843,74,374,460,438,289,46,319,838,183,217,627,387,754,710,720,520,135,54,313,901,478,664,258,849,232,369,896,509,129,466,213,256,443,86,852,901,793,814,706,301,462,234,109,886,329,160,305,772,223,751,410,212,27,589,228,528,583,940,94,790,783,797,703,172,0,295,720,320,733,953,176,375,159,141,872,16,268,224,328,90,842,743,58,723,350,174,504,874,769,39,316,503,25,347,731,629,484,777,325,929,997,119,518,605,444,776,702,903,354,382,969,534,929,185,940,294,114,648,844,625,293,270,591,176,898,724,830,164,319,53,747,667,391,364,88,337,656,114,167,598,205,31,526,130,536,321,462,843,717,851,881,337,580,421,70,404,380,390,808,813,784,176,57,594,73,894,729,722,988,483,343,913,579,384,921,269,301,362,22,709,19,78,432,4,613,993,860,171,121,158,273,451,330,573,392,930,344,261,616,325,679,223,184,348,500,908,989,423,397,163,462,908,850,242,403,955,229,302,862,498,286,333,541,883,847,655,933,620,558,842,97,796,286,596,99,157,436,153,689,286,904,411,656,129,425,519,86,394,802,193,623,511,134,620,249,863,774,299,414,705,594,84,408,735,921,305,521,648,582,957,775,214,30,545,21,729,976,495,563,335,787,434,508,116,965,656,73,934,512,662,671,371,757,200,908,691,271,468,80,339,328,537,827,333,742,996,746,735,863,41,351,32,530,393,493,556,778,629,815,754,88,729,414,61,15,702,819,924,286,21,494,877,929,435,620,668,110,698,247,544,747,923,661,909,897,208,333,273,745,526,441,297,312,313,515,763,336,909,691,923,568,562,803,959,903,796,972,993,818,113,12,778,823,505,276,0,763,820,387,900,124,41,861,503,500,480,103,786,597,329,10,738,506,917,158,369,344,53,87,333,201,378,704,611,78,916,247,736,355,135,540,486,861,349,743,144,769,577,534,684,936,655,501,904,87,349,483,736,166,39,575,597,856,249,919,761,746,676,671,852,630,957,929,428,238,126,312,582,307,947,910,941,600,682,46,512,712,626,308,747,266,655,739,724,778,873,477,45,478,545,487,477,831,646,857,813,907,812,377,793,661,418,609,183,480,47,862,997,370,253,807,99,676,744,470,137,899,603,347,377,775,4,679,125,394,622,31,714,488,573,172,889,799,23,563,691,17,916,173,873,747,49,150,529,238,3,328,940,357,896,540,245,599,643,398,959,91,133,15,37,731,926,716,705,129,442,124,605,28,939,308,969,187,921,1,330,966,633,124,674,720,904,729,322,459,993,559,10,202,82,559,586,235,240,722,296,363,785,1,112,236,401,773,397,444,102,229,48,279,59,193,597,233,620,995,29,997,421,951,945,707,233,485,692,714,40,32,677,541,958,913,472,118,525,910,46,369,63,787,376,467,491,939,426,438,372,308,891,506,385,908,319,34,505,890,213,130,718,578,607,453,222,891,42,242,542,374,886,10,445,84,501,858,277,352,166,164,197,37,577,687,608,445,175,744,96,755,641,555,822,965,977,27,409,34,962,871,735,864,32,215,65,423,318,766,332,923,835,66,161,1000,594,884,636,658,944,328,371,303,537,519,689,814,843,948,651,981,807,32,868,509,158,531,75,453,587,517,647,262,234,768,509,369,915,367,984,309,795,726,765,955,993,232,20,370,183,750,13,339,928,816,371,357,57,650,774,992,942,813,945,379,488,760,981,151,595,140,477,724,507,965,686,534,161,641,775,717,785,526,642,752,792,662,442,583,299,666,931,501,111,706,127,41,133,634,797,963,708,346,521,693,591,484,377,291,166,970,758,794,622,170,585,727,791,934,781,922,234,721,502,521,943,792,589,15,374,525,50,662,705,515,4,80,143,637,899,859,909,314,245,372,964,795,804,719,216,396,129,743,482,843,966,531,680,246,495,457,260,923,881,86,66,878,128,182,540,186,355,834,553,693,995,121,612,58,856,388,961,532,990,777,542,558,702,199,212,249,126,715,872,242,738,173,231,898,752,554,262,958,694,923,727,85,345,67,601,960,596,605,562,129,890,99,59,346,39,377,73,16,286,486,894,275,405,200,141,499,640,771,843,55,443,771,812,625,964,240,764,995,788,822,825,714,847,344,114,253,154,819,988,580,774,242,399,374,81,600,810,783,212,632,510,945,960,447,646,739,836,420,845,891,221,576,309,622,46,294,517,299,137,352,306,502,614,435,589,10,141,933,493,950,510,534,336,878,577,222,294,252,995,688,191,923,568,473,320,309,148,237,910,810,863,126,633,426,924,837,913,656,468,122,693,636,193,397,303,258,643,767,796,662,378,579,889,181,308,303,338,87,713,90,782,53,17,447,255,405,970,715,531,840,598,50,873,109,980,72,378,405,445,43,669,260,918,456,709,214,444,634,678,714,274,568,972,771,952,987,624,268,950,59,361,344,660,149,784,859,83,295,120,145,220,613,566,872,570,17,239,944,499,527,168,568,935,521,703,152,453,965,634,242,81,862,709,571,662,12,481,390,712,655,959,268,874,915,320,898,788,429,991,938,409,310,935,845,361,314,741,957,782,401,209,178,917,230,24,796,355,79,486,874,474,613,113,440,974,286,839,750,998,560,729,6,483,193,949,797,498,327,532,367,190,929,596,691,358,546,201,828,750,134,13,512,52,618,9,38,324,573,379,3,652,904,400,46,327,196,141,398,757,417,438,931,919,989,378,722,596,363,82,583,842,603,847,123,593,303,273,565,754,928,645,169,241,607,841,558,209,72,39,302,834,598,927,405,744,992,826,206,60,818,896,685,744,889,544,531,937,930,109,121,49,838,425,110,191,272,509,409,152,481,465,707,260,945,684,333,705,814,6,233,209,256,623,22,697,534,191,996,915,239,753,368,70,429,32,154,3,592,792,282,589,537,608,60,556,232,114,251,480,541,17,441,547,574,367,691,309,843,484,773,923,843,281,971,925,764,641,642,954,458,358,856,629,627,340,980,195,705,833,44,480,875,202,340,444,243,327,92,582,614,127,847,604,77,915,601,567,721,694,232,479,563,601,663,921,536,740,215,75,974,636,950,810,831,384,880,871,864,410,956,770,840,307,0,179,889,206,490,592,210,794,86,694,991,219,441,863,985,322,507,903,878,619,717,22,676,536,284,718,496,830,146,143,735,52,186,292,769,189,812,293,132,638,900,490,217,975,361,932,161,333,194,880,862,855,455,262,688,468,946,867,896,981,55,848,336,113,674,878,556,365,43,616,735,674,255,777,420,200,456,328,205,111,924,53,495,781,875,155,708,2,363,460,52,367,681,286,154,209,698,474,733,853,515,73,150,751,210,452,88,480,204,854,801,915,337,600,876,643,519,638,385,896,142,246,734,664,406,737,460,779,921,873,88,889,29,826,579,236,851,18,748,78,826,586,325,754,38,51,152,359,286,89,706,20,978,128,942,620,920,103,972,426,13,46,649,158,184,554,21,336,767,340,157,844,754,291,590,151,418,648,871,610,185,156,557,556,913,508,361,858,396,566,326,93,385,94,758,111,96,558,762,731,668,554,951,609,589,976,423,731,869,481,980,707,956,655,879,102,991,260,631,511,207,44,254,588,742,111,36,236,162,588,155,577,97,512,929,829,508,561,258,312,673,18,528,446,484,608,773,793,111,987,123,319,857,212,951,452,899,191,665,812,102,828,724,93,725,964,440,279,504,714,877,711,55,589,347,263,568,979,656,738,194,139,624,364,620,904,294,605,750,916,484,41,838,785,896,579,659,960,209,824,254,684,418,863,194,32,750,377,731,514,333,373,458,495,727,227,750,79,154,364,674,781,292,934,220,31,140,981,364,945,295,455,196,881,268,677,588,284,412,270,32,811,443,472,157,720,619,25,217,158,268,607,300,803,684,762,644,883,761,84,865,735,485,935,636,75,908,218,1000,963,193,154,453,78,693,522,815,640,622,631,360,422,206,487,429,965,706,481,213,281,352,228,86,565,690,53,528,703,994,313,758,757,401,823,176,907,251,525,64,418,902,697,541,973,899,131,72,541,506,380,445,800,269,714,345,719,274,851,529,766,542,142,726,251,375,183,364,304,610,490,541,571,676,184,917,771,988,571,995,181,263,140,429,426,416,18,593,821,497,251,437,273,323,294,155,658,481,561,940,305,545,514,775,710,959,390,979,488,443,781,296,281,885,894,455,170,897,553,194,845,29,454,2,170,619,279,4,255,212,287,693,44,993,19,850,194,233,73,544,980,342,202,398,777,607,582,389,421,372,115,771,173,626,350,847,123,617,534,935,464,687,813,611,341,100,827,508,266,407,565,933,63,18,994,862,570,396,620,49,125,414,601,32,38,781,18,401,419,50,183,285,26,428,276,690,312,912,508,84,777,728,955,810,518,447,5,77,667,712,786,455,135,580,730,144,60,297,379,923,134,884,714,664,829,135,814,229,178,792,101,866,529,504,157,216,135,565,250,724,525,103,658,633,183,210,166,218,584,584,436,977,930,325,36,337,914,200,523,412,980,236,102,948,409,36,424,868,686,36,207,691,325,368,679,282,260,395,803,862,189,754,746,312,452,528,484,542,362,298,212,491,940,809,473,928,889,738,334,215,699,539,197,645,419,799,243,359,954,573,395,447,128,432,623,882,239,658,340,727,147,520,992,773,69,549,554,920,540,444,513,191,218,679,145,874,986,523,961,294,222,940,780,292,846,162,774,178,975,476,640,310,862,309,397,713,303,736,566,475,851,730,731,222,358,241,623,420,162,712,468,323,791,744,937,644,382,784,213,85,693,99,984,61,902,33,127,42,535,41,411,114,946,115,616,177,996,799,456,495,496,904,675,366,343,387,140,54,545,916,83,467,290,245,137,469,803,228,699,31,265,458,853,11,198,140,711,677,680,500,95,997,431,501,484,221,475,227,948,627,741,670,385,950,402,842,894,712,241,172,476,172,608,348,642,705,893,110,491,899,769,292,142,712,172,989,738,292,732,241,265,785,612,686,293,226,551,978,976,750,579,907,119,427,455,79,507,605,166,85,159,293,62,942,310,233,754,505,785,730,704,253,599,784,600,878,359,467,198,550,177,675,699,573,57,524,442,38,551,870,89,242,915,261,203,152,876,369,65,921,509,879,498,339,834,672,265,775,432,108,870,395,672,931,142,183,9,110,608,256,360,465,851,183,409,876,7,843,57,324,829,879,508,238,414,427,309,721,468,108,914,795,466,256,427,57,799,285,24,963,555,837,935,202,133,90,617,295,1,632,621,391,92,320,495,224,943,931,597,753,134,475,321,686,828,797,711,759,964,960,890,197,392,515,985,416,495,324,378,356,245,413,786,318,296,84,736,73,708,889,153,173,707,445,259,945,28,653,98,418,579,257,382,897,605,179,897,976,205,645,746,988,808,641,16,257,423,726,982,294,362,687,420,383,594,930,52,559,202,875,298,658,364,736,215,766,671,113,907,29,119,785,437,576,573,34,1000,979,195,493,805,912,468,651,695,22,993,523,743,945,823,604,86,488,545,678,614,662,116,544,70,375,5,163,758,260,808,900,308,834,280,940,769,762,282,401,596,658,518,153,191,142,562,875,375,359,41,614,923,533,455,732,305,38,632,836,360,882,792,817,269,390,400,252,684,69,927,704,424,379,932,41,406,944,11,322,580,571,111,630,379,704,220,777,735,713,752,703,756,978,192,822,502,507,891,81,1000,661,213,916,678,253,778,704,796,903,210,747,38,213,489,697,882,131,275,190,507,918,455,100,273,888,473,146,81,293,471,33,803,117,747,968,837,151,684,418,974,42,596,375,728,189,235,877,799,643,827,501,316,142,463,949,736,765,853,880,1000,605,548,240,94,769,290,564,461,824,720,836,920,561,225,320,875,852,52,860,781,265,791,208,78,953,125,372,913,167,606,823,217,741,117,450,784,992,783,639,804,947,150,636,687,608,783,960,129,379,270,707,506,155,504,295,620,596,939,16,83,169,460,329,495,498,286,826,359,964,253,383,433,151,222,418,672,701,848,211,285,831,21,350,831,931,622,207,836,680,712,143,326,536,386,331,674,321,211,678,498,958,35,908,984,626,959,181,341,589,737,780,474,816,463,406,803,607,692,96,64,268,127,741,688,568,12,780,385,660,645,284,256,42,970,358,712,101,624,224,38,370,266,823,546,910,482,517,708,672,614,379,143,423,984,15,206,969,893,811,985,134,985,596,239,323,956,383,454,277,140,72,333,837,820,695,800,724,791,843,889,387,331,335,821,404,657,642,467,103,288,364,646,549,472,6,410,549,770,729,31,317,298,70,593,710,568,946,191,916,52,507,997,460,370,462,784,745,269,152,756,927,125,622,551,741,400,531,185,203,94,290,734,900,991,913,596,52,974,321,742,603,126,859,193,73,559,890,247,129,987,961,27,335,837,961,949,275,436,636,89,980,941,601,288,460,72,615,551,326,690,702,878,598,766,597,273,637,430,461,303,795,165,368,833,248,510,707,468,498,852,529,998,999,848,577,857,329,737,74,516,231,121,700,669,547,336,759,669,885,222,744,155,424,68,319,88,51,277,141,238,268,83,990,894,94,613,910,26,35,403,574,342,202,1000,499,650,431,333,697,275,533,853,288,591,485,719,415,903,853,495,804,234,882,439,870,812,408,687,810,4,999,856,287,458,935,440,377,376,165,355,309,955,124,690,57,429,367,986,517,858,218,510,988,855,738,430,319,47,794,902,589,998,224,45,272,429,647,999,620,326,463,474,493,380,40,216,741,87,180,443,513,890,997,89,485,991,325,827,369,885,562,605,759,173,432,647,93,171,413,581,398,39,112,85,980,702,215,432,22,720,645,820,380,814,300,238,102,621,937,56,968,473,107,450,380,596,440,901,768,573,391,544,101,289,896,109,444,63,78,839,937,846,903,62,465,974,507,680,408,327,336,861,436,196,462,834,975,296,873,943,934,17,203,825,393,846,612,923,71,574,942,706,245,925,347,747,53,899,17,77,586,705,312,500,642,962,684,849,87,83,237,858,780,475,503,237,636,146,392,982,225,799,762,856,901,632,207,272,137,943,248,125,202,612,225,996,119,906,172,132,773,815,928,13,231,828,760,391,216,327,25,94,149,170,450,697,516,893,679,955,941,252,641,898,303,648,57,434,367,751,109,483,827,140,732,275,972,31,496,614,415,917,84,949,185,196,517,965,724,710,620,266,118,482,256,613,930,953,546,825,251,59,974,106,100,223,958,365,135,46,391,984,310,772,739,145,557,562,496,617,84,527,786,708,33,44,510,0,390,917,214,635,919,221,381,683,176,356,30,36,958,267,212,242,996,344,866,334,652,176,120,547,574,361,892,167,182,54,623,500,43,152,663,707,855,342,351,796,155,907,712,370,621,638,335,517,204,150,174,137,600,428,349,223,35,621,535,520,515,643,566,802,667,774,412,752,634,911,827,795,773,994,548,365,936,543,668,854,607,763,617,246,94,74,661,309,137,307,393,624,853,280,547,769,932,382,245,662,347,321,502,354,210,965,884,192,610,623,942,24,515,823,483,11,495,293,489,538,679,992,963,677,998,278,251,771,133,177,314,326,505,355,33,802,471,507,681,5,816,910,456,746,311,453,274,812,228,418,397,874,429,381,233,706,252,6,389,661,483,212,47,30,990,569,770,765,563,952,4,878,278,890,647,557,484,684,147,424,962,488,855,560,954,44,225,250,116,545,85,764,412,209,787,508,592,410,895,790,91,703,365,425,800,818,991,930,234,802,204,586,745,324,371,956,471,845,18,957,31,146,715,307,35,460,951,662,452,725,200,962,132,660,546,128,497,879,926,412,198,83,384,944,655,982,688,444,63,861,292,939,878,342,114,762,85,10,279,55,514,161,938,33,997,683,420,230,52,595,805,402,794,963,0,41,382,316,486,138,834,164,824,7,562,149,699,527,453,72,228,539,594,604,260,184,860,376,369,160,917,449,963,582,278,23,294,951,471,248,165,381,398,513,555,56,438,920,872,245,251,193,797,952,994,421,377,74,91,506,836,707,513,952,755,444,119,956,487,121,444,837,257,428,196,417,98,584,864,245,680,737,853,523,34,155,625,747,572,193,407,187,79,228,304,767,226,236,91,243,632,950,413,765,650,972,688,321,256,735,113,776,595,985,917,677,954,297,894,769,584,882,236,445,95,294,38,800,216,199,556,230,159,35,424,698,849,983,587,242,980,101,872,899,181,185,742,86,901,374,430,38,743,600,869,347,250,78,697,234,120,896,631,671,5,291,57,694,882,955,705,630,613,791,978,618,830,23,257,614,247,815,50,313,991,350,320,97,300,342,711,901,628,372,44,283,622,503,310,49,481,557,880,519,643,239,946,48,714,67,528,191,960,775,70,694,104,362,16,598,40,241,896,52,252,315,590,841,862,810,792,927,821,893,162,829,685,712,859,865,835,289,673,727,284,416,36,596,791,324,724,583,203,508,559,763,672,12,645,912,438,815,909,471,166,170,837,58,172,819,978,350,166,204,853,364,10,404,315,914,601,709,788,547,189,340,457,599,222,800,88,815,943,36,559,568,601,350,840,84,326,681,961,288,554,351,833,452,855,989,61,277,923,83,871,828,266,11,501,137,928,249,493,557,583,128,976,966,242,180,911,678,900,515,48,45,333,621,185,648,417,768,738,492,446,65,384,110,554,282,652,17,997,736,580,133,95,988,262,119,941,170,780,111,710,25,815,402,663,824,237,486,42,386,814,890,783,906,361,464,311,768,579,204,909,215,855,807,499,400,159,326,297,362,332,35,536,93,212,636,129,623,542,954,114,817,83,253,370,67,71,855,836,24,139,213,454,886,906,521,442,441,437,684,954,655,121,548,575,298,190,95,28,412,278,936,631,674,531,712,926,385,73,214,813,518,122,572,476,937,205,456,987,841,542,107,286,394,134,834,237,48,360,491,313,307,846,594,151,282,70,591,957,424,130,843,133,914,992,584,669,68,403,94,807,259,629,210,457,705,961,491,209,148,211,630,764,162,256,789,463,401,107,476,952,977,751,755,107,265,954,260,11,774,75,323,465,186,215,128,213,369,761,553,594,179,250,609,851,281,231,848,567,905,384,543,116,312,667,849,733,536,479,352,824,108,149,149,6,108,644,492,139,703,398,890,704,704,651,902,460,661,688,23,974,721,738,690,146,387,428,552,82,547,461,195,367,168,872,494,205,722,234,797,876,432,26,382,983,902,481,169,287,934,653,281,246,963,199,364,595,409,986,729,614,59,573,346,621,432,549,406,905,85,596,332,99,794,599,701,925,469,468,271,507,94,796,704,892,486,424,476,833,459,668,419,62,652,171,624,911,310,401,500,243,705,157,298,750,518,572,280,688,978,308,765,422,367,138,177,160,222,330,291,714,865,786,496,33,93,746,999,684,560,99,258,444,379,21,676,96,258,996,444,433,412,648,844,252,790,739,477,24,327,80,568,981,85,602,953,63,229,204,440,183,569,408,233,601,905,821,766,38,976,265,580,548,549,491,130,6,209,728,39,648,823,546,30,644,745,624,630,784,41,283,816,343,297,279,351,68,133,329,313,369,543,771,826,648,856,596,402,348,121,5,526,435,425,603,624,48,855,969,677,364,22,846,531,271,655,148,794,944,310,459,399,116,298,126,688,169,810,514,909,915,165,479,998,476,247,915,190,408,930,98,816,354,259,756,331,960,973,725,65,919,676,674,38,388,279,125,422,258,868,275,253,49,628,570,453,310,90,789,979,343,46,985,355,575,571,97,403,127,562,878,856,523,579,689,820,496,693,784,899,568,759,473,441,335,592,654,995,609,114,781,355,926,585,279,17,69,410,476,732,115,279,452,656,239,273,174,22,54,56,379,204,261,463,838,216,70,209,854,806,837,847,269,259,429,647,547,592,186,143,178,342,878,903,237,612,670,596,83,386,112,526,433,675,876,914,879,992,213,12,824,375,499,573,506,512,466,658,268,556,588,810,581,485,265,231,761,695,701,636,159,636,438,376,665,952,372,247,609,855,226,15,912,930,327,932,960,777,985,223,208,153,39,961,418,890,390,122,985,160,24,816,885,64,10,933,703,833,943,952,957,96,7,109,108,898,467,29,30,495,434,353,673,86,990,847,887,739,706,439,766,190,939,970,78,558,731,108,294,954,575,810,917,804,544,268,701,203,474,93,952,738,961,938,943,267,442,974,88,49,722,433,819,409,496,454,763,670,690,527,359,64,473,695,128,97,832,14,617,407,725,497,272,248,877,577,857,242,384,330,478,732,901,598,601,546,994,338,112,118,152,422,656,99,820,897,384,621,328,525,773,56,514,925,817,452,125,527,196,19,177,702,780,139,387,430,402,632,840,146,382,527,594,327,386,929,226,797,746,702,83,947,969,94,254,94,297,729,49,328,711,389,723,275,3,306,578,531,747,418,579,593,460,938,841,7,616,849,506,764,18,268,758,196,386,229,635,464,563,636,366,124,471,129,76,638,461,650,688,926,697,321,793,442,287,657,339,287,370,359,399,123,562,301,326,347,267,890,117,538,547,583,28,944,693,468,810,610,501,760,608,758,204,727]

        max_rand = len(measure_values) - 1
        if max_rand >= 0:
            for stakeholder in meeting.meetingstakeholder_set.all():
                for meeting_item in meeting.meetingitem_set.all():
                    for factor in meeting.deliverable.factors.all():
                        if pseudo_random_push:
                            if pseudo_random_push == -1:
                                measure_value_index = true_random.pop() % len(measure_values)
                            else:
                                measure_value_index = random.randint(0, max_rand)
                                if measure_value_index == pseudo_random_push:
                                    measure_value_index = random.randint(0, max_rand)
                        else:
                            measure_value_index = random.randint(0, max_rand)
                        Evaluation.objects.create(
                            meeting=meeting,
                            meeting_item=meeting_item,
                            user=stakeholder.stakeholder,
                            factor=factor,
                            measure=measure,
                            measure_value=measure_values[measure_value_index],
                            evaluated_at=timezone.now()
                            )
                    meeting_item.calculate_ranking()
    else:
        print('Not enough arguments.')

if __name__ == '__main__':
    main()