from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  
from py3dbp import Packer, Bin, Item, Painter
import time

app = Flask(__name__)
CORS(app)  

BASE_BOX_DIM = 30

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_packing', methods=['POST'])
def calculate_packing():
    data = request.json
    boxes = data.get('boxes')

    # boxes = sorted(boxes, key=lambda box: box['length'] * box['width'] * box['height'], reverse=True)

    packed_boxes = []
    # occupied_spaces = []
    placement_status = [] 

    packer = Packer()

    box = Bin(
        partno='Bin',
        WHD=(BASE_BOX_DIM,BASE_BOX_DIM,BASE_BOX_DIM),
        max_weight=10000,
        corner=0,
        put_type=0
        )
    
    packer.addBin(box)

    for i, i_box in enumerate(boxes) :
        print(i, i_box)
        print((str(i+1)))

        print(i_box['width'],i_box['height'],i_box['length'])
        packer.addItem(Item(
            partno = str(i+1),
            name = 'Box',
            typeof = 'cube',
            WHD = (i_box['width'],i_box['height'],i_box['length']), 
            weight = 10,
            level = 1,
            loadbear = 10,
            updown = True,
            color = '#FF0000')
        )

    packer.pack(
        bigger_first=True,
        distribute_items=False,
        fix_point=True,
        check_stable=True,
        support_surface_ratio=0.75,
        # binding=[('server','cabint','wash')],
        # binding=['cabint','wash','server'],
        number_of_decimals=0
    )

    for box in packer.bins:
        for i, item in enumerate (box.items):
            x,y,z = item.position
            [w,h,d] = item.getDimension()
            print(x,y,z,w,h,d)
            packed_boxes.append({
                'id': i,
                'x': int(x),
                'y': int(y),
                'z': int(z),
                'width': int(w),
                'height': int(h),
                'length': int(d)
            })
        #placement_status.append({'box_index': i, 'status': 'Placed'})

    print(packed_boxes)

    return jsonify({
        'packed_boxes': packed_boxes,
        'placement_status': placement_status
    })



if __name__ == '__main__':
    app.run(debug=True)