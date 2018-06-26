from Pegasus import PictureSextet
import random


pics1 = ['bo1.jpg', 'bo2.jpg', 'bo3.jpg']
pics2 = ['bo4.jpg', 'bo5.jpg', 'bo6.jpg']
pics3 = ['bo7.jpg', 'bo8.jpg', 'bo9.jpg']
pics4 = ['bo10.jpg', 'bo11.jpg', 'bo12.jpg']
cond = random.randint(0,11)
cond2 = random.randint(0,11)
temp = PictureSextet(pics1, pics2, cond, 100) 
temp2 = PictureSextet(pics3, pics4, cond2, 100)


print("Input into PictureSextet:")
print(pics1)
print(pics2)
print(cond)
print("\nPictureSextet Tests:")
print("Pic1 Names: ", temp.trip1_names)
print("Pic2 Names: ", temp.trip2_names)
print("Overall Cond: ", temp.ovr_cond)
print("Picture Size: ", temp.pic_size)
print("Minimum Dist between pics: ", temp.min_dist)
print("Study Condition: ", temp.stu_cond)
print("Test Condition: ", temp.test_cond)
print("Is first triplet shown first: ", temp.trip1_study_first)
print("Is second triplet shown first: ", temp.trip2_study_first)
print("Triplet 1 locations: ", temp.trip1_locs)
print("Triplet 2 locations: ", temp.trip2_locs)
print("Test of print command:")
print(temp)


print('\nTest of checking overlap\n')
print("Triplet 1 locations: ", temp.trip1_locs)
print("Triplet 2 locations: ", temp.trip2_locs)
print("Triplet 3 locations: ", temp2.trip1_locs)
print("Triplet 4 locations: ", temp2.trip2_locs)

no_overlap = temp.check_dist(temp.trip1_locs + temp.trip2_locs + temp2.trip1_locs + temp2.trip2_locs)

print(no_overlap)

PictureSextet.make_compatible(temp, temp2)

no_overlap = temp.check_dist(temp.trip1_locs + temp.trip2_locs + temp2.trip1_locs + temp2.trip2_locs)

print("Triplet 3 locations: ", temp2.trip1_locs)
print("Triplet 4 locations: ", temp2.trip2_locs)

print(no_overlap)

print("Done")
