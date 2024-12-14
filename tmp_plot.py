
import numpy as np
import matplotlib.pyplot as plt

from plot_utils import create_precise_figure, save_precise_figure
from solver_wrapper import EnvModelEstimator, ScenarioParameters, SolverParameters, default_optim_factory

# prepare data

params = ScenarioParameters(
  params={
    'omega_0': np.array([[376.99111843]]), 
    'M_1': np.array([[100.]]), 
    'D_1': np.array([[10.]]), 
    'V_field_1': np.array([[2.04379375]]), 
    'P_mech_1': np.array([[-0.49936713]]), 
    'M_2': np.array([[13.2]]), 
    'D_2': np.array([[11.]]), 
    'V_field_2': np.array([[2.18712607]]), 
    'P_mech_2': np.array([[0.55]]), 
    'G_11': np.array([[0.00339983]]), 
    'G_22': np.array([[0.00339983]]), 
    'G_12': np.array([[-0.00373981]]), 
    'B_12': np.array([[-0.64137761]])}, 
  inputs={
    'y': np.array([[0.],[0.],[0.],[0.]])}, 
  network_path='./network_2bus2gen_ode.m', 
  network_name='network_2bus2gen_ode', 
  t=np.load('./trace_t.npy'), # (N, )
  x0=np.array([0.40567914, 0.        , 0.09472984, 0.        ]), 
  true_x=np.load('./trace_x.npy'), # (N, 4)
  all_params=[
    'omega_0', 
    'M_1', 'D_1', 'V_field_1', 'P_mech_1', 
    'M_2', 'D_2', 'V_field_2', 'P_mech_2', 
    'G_11', 'G_22', 'G_12', 'B_12'
  ], 
  normal_params=['M_2', 'D_2', 'V_field_2'], 
  special_params=['P_mech_2', 'G_12', 'B_12'], 
  clamp_params=['M_2', 'D_2', 'V_field_2', 'P_mech_2'], 
  observable_y_indices=np.array([0, 1])
)

sol_params = SolverParameters(
  device='cpu', 
  optim_factory=default_optim_factory, 
  batch_time=30, 
  batch_size=20, 
  ode_params={'method': 'rk4'}
)

fake_params = dict(
  M_2= 11.9997,
  D_2= 10.0060, 
  V_field_2= 1.8590, 
  P_mech_2= 0.4986,
  G_12= -0.0036, 
  B_12= -0.6238,
)

for k, v in fake_params.items():
  params.params[k][0, 0] = v
  
# construct model
estimator = EnvModelEstimator(params, sol_params)
estimator.init()

pred_x = estimator.get_response()

# plot

t = params.t
true_x = params.true_x

true_x1 = true_x[:, 0]
pred_x1 = pred_x[:, 0]
true_x2 = true_x[:, 2]
pred_x2 = pred_x[:, 2]

fig, ax = create_precise_figure(
  width_cm=7.8,
  height_cm=3.7,
  font_size_pt=7,
  scale_factor=2,
  margin_cm=0.01,
  latex_mode=True,
)

ax.plot(t, true_x1, label='$\\theta_1$')
ax.plot(t, pred_x1, '--', label='$\\theta_1$ (estimated)')
ax.plot(t, true_x2, label='$\\theta_2$')
ax.plot(t, pred_x2, '--', label='$\\theta_2$ (estimated)')
ax.set_xlabel('Time')
ax.set_ylabel('Value')
# ax.set_title('Rotor Angle')
ax.legend()
ax.grid(True)

save_precise_figure(
  fig,
  'run/output_figure',
  dpi=300,
  formats=['pdf', 'png', 'svg'],
  transparent=False,
)