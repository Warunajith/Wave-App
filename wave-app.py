import pandas as pd
from h2o_wave import main, app, Q, ui
from h2o_wave_ml import build_model

dataset = 'Bengaluru_House_Data.csv'

model = build_model(train_file_path=dataset, target_column='price')

# Load the dataset using pandas
df = pd.read_csv(dataset)

# Get a list of unique values of a particular column and prepare choices for dropdown component
features = ['area_type', 'location', 'size', 'bathrooms', 'balcony', 'total_sqft']
columns = {f: df[f].unique().tolist() for f in features}
choices = {key: [ui.choice(str(item)) for item in columns[key] if not pd.isnull(item)] for key in columns}

# Extract a default row
default_row = df.iloc[2].to_dict()
default_value = {key: cols[0] for key, cols in default_row.items()}

@app('/predict')
async def serve(q: Q):

    # Prepare feature values or use default ones
    area_type = q.args.country or default_value['area_type']
    location = q.args.price if q.args.price else default_value['location']
    size = q.args.province or default_value['size']
    bathrooms = q.args.region or default_value['bathrooms']
    balcony = q.args.variety or default_value['balcony']
    total_sqft = q.args.winery or default_value['total_sqft']

    # Prepare input data and do the predictions
    input_data = [[area_type, location, size, bathrooms, balcony, total_sqft]]
    price = model.predict(input_data)
    price = int(price[0][0])

    # Initialize page with a layout
    if not q.client.initialized:
        q.page['meta'] = ui.meta_card(box='', layouts=[
            ui.layout(
                breakpoint='xs',
                width='576px',
                zones=[ui.zone('body')],
            )
        ])
        q.page['header'] = ui.header_card(
            box='body',
            title='Real State Price Predictor'

        )
        q.page['result'] = ui.tall_gauge_stat_card(
            box=ui.box('body', height='180px'),
            title='',
            value=str(price),
            aux_value='price',
            plot_color='$red'

        )
        q.page['predict'] = ui.form_card(box='body', items=[
            ui.dropdown(name='area_type', label='Area Type', value=area_type, trigger=True, choices=choices['area_type']),
            ui.dropdown(name='location', label='Location', value=location, trigger=True, choices=choices['location']),
            ui.dropdown(name='size', label='Size', value=size, trigger=True, choices=choices['size']),
            ui.dropdown(name='bathrooms', label='Bathrooms', value=bathrooms, trigger=True, choices=choices['bathrooms']),
            ui.dropdown(name='balcony', label='Balcony', value=balcony, trigger=True, choices=choices['balcony']),
            ui.slider(name='total_sqft', label='Total SQFT', min=4, max=150, step=1, value=float(total_sqft), trigger=True),
        ])
        q.client.initialized = True
    else:
        q.page['result'].value = str(price)
        q.page['result'].plot_color = '$red'

    await q.page.save()